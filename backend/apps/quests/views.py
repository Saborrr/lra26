from django.db import transaction
from rest_framework import viewsets

from api.permissions import IsAdminOrReadOnly
from apps.accounts.services import audit

from .models import Quest
from .serializers import QuestListSerializer, QuestSerializer


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "active"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_authenticated and self.request.user.is_staff):
            queryset = queryset.filter(active=True)
        return queryset

    def get_serializer_class(self):
        return QuestListSerializer if self.action in {"list", "retrieve"} else QuestSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        obj = serializer.save()
        audit(action="quest.create", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        audit(action="quest.update", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_destroy(self, instance):
        audit(action="quest.delete", actor=self.request.user, target=instance, request=self.request)
        instance.delete()
