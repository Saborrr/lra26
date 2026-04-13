"""Сериализаторы для результатов."""

from rest_framework import serializers

from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    """Полный сериализатор результата."""

    team_name = serializers.CharField(source="team.name", read_only=True)
    quest_title = serializers.CharField(source="quest.title", read_only=True)
    entered_by_name = serializers.CharField(
        source="entered_by.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Score
        fields = [
            "id",
            "team",
            "team_name",
            "quest",
            "quest_title",
            "points",
            "verified",
            "entered_by",
            "entered_by_name",
            "notes",
            "timestamp",
        ]
        read_only_fields = ["timestamp"]


class ScoreListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка результатов."""

    team_name = serializers.CharField(source="team.name", read_only=True)
    quest_title = serializers.CharField(source="quest.title", read_only=True)

    class Meta:
        model = Score
        fields = [
            "id",
            "team",
            "team_name",
            "quest",
            "quest_title",
            "points",
            "verified",
            "timestamp",
        ]


class ScoreCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания результата."""

    class Meta:
        model = Score
        fields = ["team", "quest", "points", "notes"]