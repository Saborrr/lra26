from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.penalties.models import BlackMark
from apps.scores.models import Score

from .models import Team


def leaderboard_payload():
    from api.views import leaderboard_teams

    from .serializers import TeamLeaderboardSerializer

    return TeamLeaderboardSerializer(leaderboard_teams(), many=True).data


def broadcast_leaderboard():
    layer = get_channel_layer()
    if layer:
        async_to_sync(layer.group_send)(
            "leaderboard",
            {"type": "score_update", "teams": leaderboard_payload()},
        )


def recalculate_teams(team_ids):
    ids = sorted({team_id for team_id in team_ids if team_id})
    if not ids:
        return
    with transaction.atomic():
        teams = Team.objects.select_for_update().filter(pk__in=ids).order_by("pk")
        for team in teams:
            score = team.scores.aggregate(total=Sum("points"))["total"] or 0
            penalty = team.black_marks.aggregate(total=Sum("penalty"))["total"] or 0
            Team.objects.filter(pk=team.pk).update(score=score, penalty=penalty)


def remember_previous_team(instance, model):
    instance._previous_team_id = None
    if instance.pk:
        instance._previous_team_id = (
            model.objects.filter(pk=instance.pk).values_list("team_id", flat=True).first()
        )


def schedule_broadcast():
    transaction.on_commit(broadcast_leaderboard)


@receiver(pre_save, sender=Score)
def score_before_save(sender, instance, **kwargs):
    remember_previous_team(instance, Score)


@receiver(post_save, sender=Score)
def score_saved(sender, instance, **kwargs):
    recalculate_teams([instance.team_id, getattr(instance, "_previous_team_id", None)])
    schedule_broadcast()


@receiver(post_delete, sender=Score)
def score_deleted(sender, instance, **kwargs):
    recalculate_teams([instance.team_id])
    schedule_broadcast()


@receiver(pre_save, sender=BlackMark)
def penalty_before_save(sender, instance, **kwargs):
    remember_previous_team(instance, BlackMark)


@receiver(post_save, sender=BlackMark)
def penalty_saved(sender, instance, **kwargs):
    recalculate_teams([instance.team_id, getattr(instance, "_previous_team_id", None)])
    schedule_broadcast()


@receiver(post_delete, sender=BlackMark)
def penalty_deleted(sender, instance, **kwargs):
    recalculate_teams([instance.team_id])
    schedule_broadcast()
