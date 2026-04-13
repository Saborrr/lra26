"""URL-маршруты для штрафов."""

from rest_framework.routers import SimpleRouter

from .views import BlackMarkViewSet

router = SimpleRouter()
router.register(r"", BlackMarkViewSet, basename="blackmark")

urlpatterns = router.urls