"""Кастомные API views."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.teams.models import Team
from apps.teams.serializers import TeamLeaderboardSerializer


class LeaderboardView(APIView):
    """Возвращает отсортированный рейтинг команд."""

    permission_classes = []

    def get(self, request):
        """Получить рейтинг команд."""
        teams = (
            Team.objects.select_related("trainer")
            .prefetch_related("scores")
            .all()
        )
        # Сортируем по итоговому баллу (score - penalty)
        teams = sorted(teams, key=lambda t: t.score - t.penalty, reverse=True)
        serializer = TeamLeaderboardSerializer(teams, many=True)
        return Response(serializer.data)


class MyTeamView(APIView):
    """Возвращает команду текущего тренера."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получить команду тренера."""
        user = request.user
        try:
            trainer = user.trainer
        except AttributeError:
            return Response({"error": "Пользователь не является тренером"}, status=403)

        teams = trainer.teams.select_related("trainer").prefetch_related("scores")
        serializer = TeamLeaderboardSerializer(teams, many=True)
        return Response(serializer.data)