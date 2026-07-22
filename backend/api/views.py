from django.db import connection
from django.db.models import F, IntegerField, Value
from django.db.models.functions import Coalesce
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.teams.models import Team
from apps.teams.serializers import TeamLeaderboardSerializer


def leaderboard_teams():
    teams = list(
        Team.objects.select_related("trainer")
        .annotate(
            calculated_total=Coalesce(F("score"), Value(0), output_field=IntegerField())
            - Coalesce(F("penalty"), Value(0), output_field=IntegerField())
        )
        .order_by("-calculated_total", "name")
    )
    last_score = None
    rank = 0
    for index, team in enumerate(teams, 1):
        if team.calculated_total != last_score:
            rank = index
            last_score = team.calculated_total
        team.leaderboard_position = rank
    return teams


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return Response({"status": "ok"})


class LeaderboardView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        serializer = TeamLeaderboardSerializer(leaderboard_teams(), many=True)
        return Response(serializer.data)


class MyTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = getattr(request.user, "trainer", None)
        if trainer is None:
            return Response({"detail": "К профилю не привязан участник"}, status=404)
        teams = trainer.teams.select_related("trainer").prefetch_related("scores__quest")
        return Response(TeamLeaderboardSerializer(teams, many=True).data)
