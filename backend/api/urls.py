from django.urls import include, path

from api.views import HealthView, LeaderboardView, MyTeamView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("auth/", include("apps.accounts.urls")),
    path("teams/", include("apps.teams.urls")),
    path("scores/", include("apps.scores.urls")),
    path("quests/", include("apps.quests.urls")),
    path("trainers/", include("apps.trainers.urls")),
    path("marks/", include("apps.penalties.urls")),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("my-team/", MyTeamView.as_view(), name="my-team"),
]
