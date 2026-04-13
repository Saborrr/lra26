"""Сериализаторы для команд."""

from rest_framework import serializers

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    """Полный сериализатор команды."""

    trainer_name = serializers.CharField(
        source="trainer.name", read_only=True, allow_null=True
    )
    scores_count = serializers.SerializerMethodField()
    total_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "trainer",
            "trainer_name",
            "score",
            "penalty",
            "color",
            "logo",
            "position",
            "scores_count",
            "total_score",
        ]
        read_only_fields = ["score", "penalty", "position"]

    def get_scores_count(self, obj):
        """Возвращает количество результатов команды."""
        return obj.scores.count()


class TeamListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка команд."""

    trainer_name = serializers.CharField(
        source="trainer.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "trainer_name",
            "score",
            "penalty",
            "color",
            "position",
        ]


class TeamLeaderboardSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга."""

    trainer_name = serializers.CharField(
        source="trainer.name", read_only=True, allow_null=True
    )
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "trainer_name",
            "score",
            "penalty",
            "total_score",
            "color",
            "position",
        ]

    def get_total_score(self, obj):
        """Возвращает итоговый балл (score - penalty)."""
        return obj.score - obj.penalty