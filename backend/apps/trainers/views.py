"""Views для тренеров."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Trainer
from .serializers import (
    TrainerCreateSerializer,
    TrainerListSerializer,
    TrainerSerializer,
)


class TrainerViewSet(viewsets.ModelViewSet):
    """ViewSet для тренеров.

    Чтение доступно всем, создание/редактирование - только админам.
    """

    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "telegram_id"]
    ordering = ["name"]

    def get_serializer_class(self):
        """Возвращает разные сериализаторы для разных действий."""
        if self.action == "list":
            return TrainerListSerializer
        if self.action == "create":
            return TrainerCreateSerializer
        return super().get_serializer_class()