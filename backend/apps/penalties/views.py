from django.db import transaction
from rest_framework import viewsets

from api.permissions import IsAdmin
from apps.accounts.services import audit

from .models import BlackMark
from .serializers import BlackMarkSerializer


class BlackMarkViewSet(viewsets.ModelViewSet):
    queryset = BlackMark.objects.select_related("team", "given_by").all()
    serializer_class = BlackMarkSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ["team"]

    @transaction.atomic
    def perform_create(self, serializer):
        obj = serializer.save(given_by=getattr(self.request.user, "trainer", None))
        audit(
            action="penalty.create",
            actor=self.request.user,
            target=obj,
            request=self.request,
            metadata={"penalty": obj.penalty},
        )

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        audit(
            action="penalty.update",
            actor=self.request.user,
            target=obj,
            request=self.request,
            metadata={"penalty": obj.penalty},
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        audit(
            action="penalty.delete", actor=self.request.user, target=instance, request=self.request
        )
        instance.delete()
