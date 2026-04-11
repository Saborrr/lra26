from rest_framework.routers import DefaultRouter

from .views import TeamViewSet


router = DefaultRouter()
router.register(r"", TeamViewSet)

urlpatterns = router.urls