from rest_framework.routers import DefaultRouter

from .views import ScoreViewSet


router = DefaultRouter()
router.register(r"", ScoreViewSet)

urlpatterns = router.urls