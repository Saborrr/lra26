"""Views для штрафов."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import BlackMark
from .serializers import BlackMarkListSerializer, BlackMarkSerializer


class BlackMarkViewSet(viewsets.ModelViewSet):
    """ViewSet для штрафов (чёрных меток).

    Только админы могут управлять штрафами.
    """

    queryset = BlackMark.objects.select_related("team", "given_by").all()
    serializer_class = BlackMarkSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["team", "given_by"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Возвращает краткий сериализатор для списка."""
        if self.action == "list":
            return BlackMarkListSerializer
        return super().get_serializer_class()