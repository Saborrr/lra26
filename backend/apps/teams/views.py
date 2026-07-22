from django.db import transaction
from rest_framework import viewsets

from api.permissions import IsAdminOrReadOnly
from apps.accounts.services import audit

from .models import Team
from .serializers import TeamListSerializer, TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.select_related("trainer").all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["trainer"]

    def get_serializer_class(self):
        return TeamListSerializer if self.action in {"list", "retrieve"} else TeamSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        obj = serializer.save()
        audit(action="team.create", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        audit(action="team.update", actor=self.request.user, target=obj, request=self.request)

    @transaction.atomic
    def perform_destroy(self, instance):
        audit(action="team.delete", actor=self.request.user, target=instance, request=self.request)
        instance.delete()
