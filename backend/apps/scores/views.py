from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.permissions import IsAdmin
from apps.accounts.services import audit

from .models import Score
from .serializers import ScoreSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related("team", "quest", "entered_by").all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ["team", "quest", "verified"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        incoming = self.get_serializer(data=request.data)
        incoming.is_valid(raise_exception=True)
        team = incoming.validated_data["team"]
        quest = incoming.validated_data["quest"]

        # Locking the team serializes concurrent writes for the same scoreboard row.
        team.__class__.objects.select_for_update().get(pk=team.pk)
        instance = Score.objects.filter(team=team, quest=quest).first()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_status = status.HTTP_200_OK
        else:
            serializer = incoming
            self.perform_create(serializer)
            response_status = status.HTTP_201_CREATED
        return Response(serializer.data, status=response_status)

    @transaction.atomic
    def perform_create(self, serializer):
        trainer = getattr(self.request.user, "trainer", None)
        obj = serializer.save(entered_by=trainer)
        audit(
            action="score.create",
            actor=self.request.user,
            target=obj,
            request=self.request,
            metadata={"points": obj.points},
        )

    @transaction.atomic
    def perform_update(self, serializer):
        obj = serializer.save()
        audit(
            action="score.update",
            actor=self.request.user,
            target=obj,
            request=self.request,
            metadata={"points": obj.points},
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        audit(action="score.delete", actor=self.request.user, target=instance, request=self.request)
        instance.delete()
