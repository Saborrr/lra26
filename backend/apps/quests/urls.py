"""URL-маршруты для квестов."""

from rest_framework.routers import SimpleRouter

from .views import QuestViewSet

router = SimpleRouter()
router.register(r"", QuestViewSet, basename="quest")

urlpatterns = router.urls
