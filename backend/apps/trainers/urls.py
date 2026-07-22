"""URL-маршруты для тренеров."""

from rest_framework.routers import SimpleRouter

from .views import TrainerViewSet

router = SimpleRouter()
router.register(r"", TrainerViewSet, basename="trainer")

urlpatterns = router.urls
