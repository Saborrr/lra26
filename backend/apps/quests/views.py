"""Views для квестов."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from .models import Quest
from .serializers import QuestListSerializer, QuestSerializer


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Разрешает чтение всем, редактирование только админам."""

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user and request.user.is_staff


class QuestViewSet(viewsets.ModelViewSet):
    """ViewSet для квестов."""

    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "is_active"]
    ordering = ["order", "title"]

    def get_serializer_class(self):
        """Возвращает краткий сериализатор для списка."""
        if self.action == "list":
            return QuestListSerializer
        return super().get_serializer_class()