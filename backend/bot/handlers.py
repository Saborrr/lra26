"""Обработчики команд Telegram-бота."""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from django.conf import settings
from apps.teams.models import Team
from apps.trainers.models import Trainer
from apps.quests.models import Quest
from apps.scores.models import Score


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - приветствие."""
    await update.message.reply_text(
        "🚀 *ЛРА-2026 — Рейтинг команд*\n\n"
        "Добро пожаловать в систему Live-рейтинга!\n\n"
        "Доступные команды:\n"
        "/teams — Топ-10 команд\n"
        "/myteam — Информация о вашей команде\n"
        "/addscore — Внести результат\n"
        "/login <код> — Привязать Telegram\n\n"
        "Слёт лидеров: 27-29.05.2026",
        parse_mode="Markdown",
    )


async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /teams - топ-10 команд."""
    all_teams = list(Team.objects.select_related("trainer").all())
    # Сортируем по итоговому баллу
    all_teams.sort(key=lambda t: t.score - t.penalty, reverse=True)
    top_10 = all_teams[:10]

    message = "🏆 *Топ-10 команд*\n\n"
    for i, team in enumerate(top_10, 1):
        total = team.score - team.penalty
        trainer = team.trainer.name if team.trainer else "—"
        message += f"{i}. *{team.name}* — {total} очков\n"
        message += f"   📊 Тренер: {trainer}\n"
        if team.penalty > 0:
            message += f"   ⚠️ Штраф: {team.penalty}\n"

    await update.message.reply_text(message, parse_mode="Markdown")


async def myteam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /myteam - информация о команде тренера."""
    telegram_id = update.effective_user.id

    try:
        trainer = Trainer.objects.get(telegram_id=telegram_id)
    except Trainer.DoesNotExist:
        await update.message.reply_text(
            "❌ Вы не привязаны к системе.\n"
            "Используйте /login <код> для привязки аккаунта."
        )
        return

    teams_list = trainer.teams.all()
    if not teams_list:
        await update.message.reply_text("❌ У вас нет команд.")
        return

    for team in teams_list:
        total = team.score - team.penalty
        message = f"👥 *{team.name}*\n\n"
        message += f"📊 Очки: {team.score}\n"
        message += f"⚠️ Штраф: {team.penalty}\n"
        message += f"🏆 Итого: {total}\n\n"

        # Показываем результаты по квестам
        scores = team.scores.select_related("quest").all()
        if scores:
            message += "📋 Результаты:\n"
            for score in scores:
                message += f"  • {score.quest.title}: {score.points}\n"

        await update.message.reply_text(message, parse_mode="Markdown")


async def addscore(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /addscore - выбор квеста для внесения результата."""
    telegram_id = update.effective_user.id

    try:
        trainer = Trainer.objects.get(telegram_id=telegram_id)
    except Trainer.DoesNotExist:
        await update.message.reply_text(
            "❌ Вы не привязаны к системе.\n"
            "Используйте /login <код> для привязки аккаунта."
        )
        return

    teams_list = trainer.teams.all()
    if not teams_list:
        await update.message.reply_text("❌ У вас нет команд.")
        return

    # Показываем выбор команды
    keyboard = []
    for team in teams_list:
        keyboard.append([
            InlineKeyboardButton(team.name, callback_data=f"team_{team.id}")
        ])
    keyboard.append([
        InlineKeyboardButton("❌ Отмена", callback_data="cancel")
    ])

    await update.message.reply_text(
        "Выберите команду:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /login - привязка Telegram к Trainer."""
    if not context.args:
        await update.message.reply_text(
            "Использование: /login <код>\n\n"
            "Получите код у администратора."
        )
        return

    code = context.args[0]

    # Ищем тренера по временному коду (можно добавить поле login_code)
    try:
        trainer = Trainer.objects.get(telegram_id__isnull=True)
        # В реальной реализации нужна проверка кода
        trainer.telegram_id = update.effective_user.id
        trainer.save()
        await update.message.reply_text(
            f"✅ Аккаунт привязан!\n\n"
            f"Вы: {trainer.name}"
        )
    except Trainer.DoesNotExist:
        await update.message.reply_text("❌ Неверный код или аккаунт уже привязан.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатий на кнопки."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "cancel":
        await query.edit_message_text("❌ Отменено.")
        return

    if data.startswith("team_"):
        team_id = int(data.split("_")[1])
        # Показываем выбор квеста
        quests = Quest.objects.all().order_by("order")
        keyboard = []
        for quest in quests:
            keyboard.append([
                InlineKeyboardButton(
                    quest.title, callback_data=f"quest_{team_id}_{quest.id}"
                )
            ])
        keyboard.append([
            InlineKeyboardButton("❌ Отмена", callback_data="cancel")
        ])
        await query.edit_message_text(
            "Выберите квест:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data.startswith("quest_"):
        _, team_id, quest_id = data.split("_")
        # Показываем выбор баллов
        keyboard = []
        for points in [10, 20, 30, 50, 100]:
            keyboard.append([
                InlineKeyboardButton(
                    f"+{points}", callback_data=f"score_{team_id}_{quest_id}_{points}"
                )
            ])
        keyboard.append([
            InlineKeyboardButton("❌ Отмена", callback_data="cancel")
        ])
        await query.edit_message_text(
            "Выберите баллы:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data.startswith("score_"):
        _, team_id, quest_id, points = data.split("_")
        team_id = int(team_id)
        quest_id = int(quest_id)
        points = int(points)

        # Создаём или обновляем Score
        score, created = Score.objects.update_or_create(
            team_id=team_id,
            quest_id=quest_id,
            defaults={"points": points},
        )

        await query.edit_message_text(
            f"✅ Результат сохранён!\n\n"
            f"Квест: {score.quest.title}\n"
            f"Баллы: +{points}"
        )
        return


def create_application() -> Application:
    """Создаёт приложение Telegram-бота."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", settings.TELEGRAM_BOT_TOKEN)
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("teams", teams))
    application.add_handler(CommandHandler("myteam", myteam))
    application.add_handler(CommandHandler("addscore", addscore))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CallbackQueryHandler(button_callback))

    return application