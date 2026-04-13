"""
Signals for teams app.
Обновляет team.score при изменении Score,
team.penalty при изменении BlackMark,
и отправляет WebSocket broadcast.
"""
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.scores.models import Score
from apps.penalties.models import BlackMark


def update_team_score(team):
    """Пересчитывает team.score = sum(scores.points)."""
    total = team.scores.aggregate(total=Sum('points'))['total'] or 0
    team.score = total
    team.save(update_fields=['score', 'updated_at'])


def update_team_penalty(team):
    """Пересчитывает team.penalty = sum(black_marks.penalty)."""
    total = team.black_marks.aggregate(
        total=Sum('penalty')
    )['total'] or 0
    team.penalty = total
    team.save(update_fields=['penalty', 'updated_at'])


def broadcast_leaderboard():
    """Отправляет WebSocket broadcast с обновлённым рейтингом."""
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            "leaderboard",
            {"type": "score_update"}
        )


@receiver(post_save, sender=Score)
def on_score_save(sender, instance, **kwargs):
    """При сохранении Score обновляем team.score и broadcast."""
    update_team_score(instance.team)
    broadcast_leaderboard()


@receiver(post_delete, sender=Score)
def on_score_delete(sender, instance, **kwargs):
    """При удалении Score обновляем team.score и broadcast."""
    update_team_score(instance.team)
    broadcast_leaderboard()


@receiver(post_save, sender=BlackMark)
def on_blackmark_save(sender, instance, **kwargs):
    """При сохранении BlackMark обновляем team.penalty и broadcast."""
    update_team_penalty(instance.team)
    broadcast_leaderboard()


@receiver(post_delete, sender=BlackMark)
def on_blackmark_delete(sender, instance, **kwargs):
    """При удалении BlackMark обновляем team.penalty и broadcast."""
    update_team_penalty(instance.team)
    broadcast_leaderboard()