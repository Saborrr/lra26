from rest_framework import viewsets, permissions
from api.permissions import IsAdminOrReadOnly

from .models import Team
from .serializers import TeamSerializer


# ViewSet для API команд (/api/teams/)
# Поддерживает CRUD, read-only для всех, write для admin/trainer.
# Регулировать: filterset_class, pagination_class, permission_classes.
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by("-score")
    serializer_class = TeamSerializer
    permission_classes = [IsAdminOrReadOnly]
