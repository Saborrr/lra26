"""API v1 URL configuration."""

from django.urls import path, include

from api.views import LeaderboardView, MyTeamView

urlpatterns = [
    path("teams/", include("apps.teams.urls")),
    path("scores/", include("apps.scores.urls")),
    path("quests/", include("apps.quests.urls")),
    path("trainers/", include("apps.trainers.urls")),
    path("marks/", include("apps.penalties.urls")),
    # Кастомные endpoints
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("my-team/", MyTeamView.as_view(), name="my-team"),
]