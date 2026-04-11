"""API v1 URL configuration."""
from django.urls import path, include

urlpatterns = [
    path("teams/", include("apps.teams.urls")),
    path("scores/", include("apps.scores.urls")),
    path("quests/", include("apps.quests.urls")),
]