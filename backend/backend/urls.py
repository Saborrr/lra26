"""backend URL Configuration"""
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from backend.trainer_views import (
    TrainerPanelView,
    SaveScoresView,
    AddBlackMarkView,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("trainer/", TrainerPanelView.as_view(), name="trainer"),
    path("trainer/save-scores/", SaveScoresView.as_view()),
    path("trainer/add-mark/", AddBlackMarkView.as_view()),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include("api.urls")),
]
