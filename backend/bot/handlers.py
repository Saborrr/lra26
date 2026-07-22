"""Secure Telegram bot for LRA-26."""

import html
import logging

from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import ValidationError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from apps.accounts.models import PlatformIdentity
from apps.accounts.services import audit, resolve_platform_user
from apps.quests.models import Quest
from apps.scores.models import Score
from apps.teams.models import Team

logger = logging.getLogger(__name__)


@sync_to_async(thread_sensitive=True)
def telegram_user(telegram_id):
    identity = (
        PlatformIdentity.objects.select_related("user")
        .filter(provider=PlatformIdentity.Provider.TELEGRAM, external_id=str(telegram_id))
        .first()
    )
    return identity.user if identity and identity.user.is_active else None


@sync_to_async(thread_sensitive=True)
def link_telegram_user(telegram_id, display_name, code):
    return resolve_platform_user(
        provider=PlatformIdentity.Provider.TELEGRAM,
        external_id=str(telegram_id),
        display_name=display_name,
        link_code=code,
    )


@sync_to_async(thread_sensitive=True)
def top_teams():
    return list(Team.objects.select_related("trainer").order_by("-score", "penalty")[:10])


@sync_to_async(thread_sensitive=True)
def all_teams():
    return list(Team.objects.order_by("name"))


@sync_to_async(thread_sensitive=True)
def participant_teams(user):
    trainer = getattr(user, "trainer", None)
    if not trainer:
        return []
    return list(trainer.teams.prefetch_related("scores__quest").all())


@sync_to_async(thread_sensitive=True)
def active_quests():
    return list(Quest.objects.filter(active=True).order_by("order", "id"))


@sync_to_async(thread_sensitive=True)
@transaction.atomic
def save_score(user, team_id, quest_id, points):
    if not user.is_staff:
        raise PermissionError("Недостаточно прав")
    team = Team.objects.select_for_update().get(pk=team_id)
    quest = Quest.objects.get(pk=quest_id, active=True)
    if points < 0 or points > quest.points:
        raise ValueError("Баллы выходят за пределы задания")
    score, _ = Score.objects.update_or_create(
        team=team,
        quest=quest,
        defaults={
            "points": points,
            "verified": True,
            "entered_by": getattr(user, "trainer", None),
        },
    )
    audit(action="score.telegram", actor=user, target=score, metadata={"points": points})
    return score, team, quest


def display_name(update):
    user = update.effective_user
    return " ".join(part for part in [user.first_name, user.last_name] if part)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Открыть LRA-26", web_app=WebAppInfo(settings.APP_PUBLIC_URL))]]
    )
    await update.effective_message.reply_text(
        "<b>LRA-26 · Космический рейтинг</b>\n\n"
        "Следите за результатами, своей командой и заданиями прямо в Telegram.\n\n"
        "/teams — рейтинг\n"
        "/myteam — моя команда\n"
        "/login КОД — привязать аккаунт\n"
        "/addscore — внести результат (для администраторов)",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = await top_teams()
    lines = ["<b>🏆 Рейтинг команд</b>", ""]
    for index, team in enumerate(rows, 1):
        lines.append(f"{index}. <b>{html.escape(team.name)}</b> · {team.total_score}")
    await update.effective_message.reply_text("\n".join(lines), parse_mode="HTML")


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.effective_message.reply_text("Использование: /login XXXX-XXXX-XXXX")
        return
    try:
        user = await link_telegram_user(
            update.effective_user.id, display_name(update), context.args[0]
        )
    except ValidationError:
        await update.effective_message.reply_text("❌ Код неверен, истёк или уже использован.")
        return
    await update.effective_message.reply_text(
        f"✅ Аккаунт <b>{html.escape(user.username)}</b> успешно привязан.",
        parse_mode="HTML",
    )


async def myteam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await telegram_user(update.effective_user.id)
    if not user:
        await update.effective_message.reply_text("Сначала привяжите аккаунт: /login КОД")
        return
    rows = await participant_teams(user)
    if not rows:
        await update.effective_message.reply_text("К аккаунту пока не привязана команда.")
        return
    for team in rows:
        lines = [
            f"<b>👥 {html.escape(team.name)}</b>",
            f"Баллы: {team.score}",
            f"Штраф: {team.penalty}",
            f"Итого: <b>{team.total_score}</b>",
        ]
        await update.effective_message.reply_text("\n".join(lines), parse_mode="HTML")


async def addscore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await telegram_user(update.effective_user.id)
    if not user or not user.is_staff:
        await update.effective_message.reply_text("Эта команда доступна только администраторам.")
        return
    rows = await all_teams()
    keyboard = [[InlineKeyboardButton(team.name, callback_data=f"team:{team.pk}")] for team in rows]
    await update.effective_message.reply_text(
        "Выберите команду:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await telegram_user(update.effective_user.id)
    if not user or not user.is_staff:
        await query.edit_message_text("Недостаточно прав.")
        return
    kind, _, value = (query.data or "").partition(":")
    if kind == "team" and value.isdigit():
        context.user_data["team_id"] = int(value)
        quests = await active_quests()
        keyboard = [[InlineKeyboardButton(q.title, callback_data=f"quest:{q.pk}")] for q in quests]
        await query.edit_message_text(
            "Выберите задание:", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    if kind == "quest" and value:
        quests = await active_quests()
        quest = next((item for item in quests if str(item.pk) == value), None)
        if not quest:
            await query.edit_message_text("Задание больше недоступно.")
            return
        context.user_data["quest_id"] = str(quest.pk)
        steps = sorted(
            {0, quest.points // 4, quest.points // 2, (quest.points * 3) // 4, quest.points}
        )
        keyboard = [[InlineKeyboardButton(str(p), callback_data=f"points:{p}")] for p in steps]
        await query.edit_message_text(
            f"Баллы за «{html.escape(quest.title)}»:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return
    if kind == "points" and value.isdigit():
        team_id = context.user_data.get("team_id")
        quest_id = context.user_data.get("quest_id")
        if not team_id or not quest_id:
            await query.edit_message_text("Сессия выбора истекла. Запустите /addscore снова.")
            return
        try:
            _, team, quest = await save_score(user, team_id, quest_id, int(value))
        except (Team.DoesNotExist, Quest.DoesNotExist, ValueError, PermissionError):
            logger.warning("Rejected Telegram score update", extra={"user_id": user.pk})
            await query.edit_message_text("Не удалось сохранить результат.")
            return
        context.user_data.clear()
        await query.edit_message_text(
            f"✅ {html.escape(team.name)} · {html.escape(quest.title)}: <b>{value}</b>",
            parse_mode="HTML",
        )
        return
    await query.edit_message_text("Команда устарела. Запустите /addscore снова.")


def create_application():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("teams", teams))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("myteam", myteam))
    application.add_handler(CommandHandler("addscore", addscore))
    application.add_handler(CallbackQueryHandler(button_callback))
    return application
