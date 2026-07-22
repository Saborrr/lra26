from django.db import transaction
from rest_framework import viewsets

from api.permissions import IsAdmin
from apps.accounts.services import audit

from .models import Trainer
from .serializers import TrainerCreateSerializer, TrainerListSerializer, TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.select_related("user").all()
    permission_classes = [IsAdmin]
    filterset_fields = ["name", "telegram_id"]

    def get_serializer_class(self):
        if self.action == "list":
            return TrainerListSerializer
        if self.action == "create":
            return TrainerCreateSerializer
        return TrainerSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        obj = serializer.save()
        audit(action="trainer.create", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        audit(action="trainer.update", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_destroy(self, instance):
        audit(
            action="trainer.delete", actor=self.request.user, target=instance, request=self.request
        )
        instance.delete()
