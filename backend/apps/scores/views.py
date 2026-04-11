from rest_framework import viewsets, permissions
from api.permissions import IsAdminOrReadOnly

from .models import Score
from .serializers import ScoreSerializer


# ViewSet для API счетов (/api/scores/)
# CRUD для результатов квестов, read-only все, write admin.
# Регулировать: filter_backends (по team/quest), permission.
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAdminOrReadOnly]
