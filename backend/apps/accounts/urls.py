from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AuditEventViewSet,
    LoginCodeViewSet,
    LoginView,
    LogoutView,
    MeView,
    ParticipantDirectoryView,
    RefreshView,
    TelegramAuthView,
    UserViewSet,
    VkAuthView,
)

router = SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("link-codes", LoginCodeViewSet, basename="link-code")
router.register("audit", AuditEventViewSet, basename="audit-event")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("participants/", ParticipantDirectoryView.as_view(), name="participant-directory"),
    path("telegram/", TelegramAuthView.as_view(), name="telegram-auth"),
    path("vk/", VkAuthView.as_view(), name="vk-auth"),
    path("", include(router.urls)),
]
