"""Сериализаторы для штрафов."""

from rest_framework import serializers

from .models import BlackMark


class BlackMarkSerializer(serializers.ModelSerializer):
    """Полный сериализатор штрафа."""

    team_name = serializers.CharField(source="team.name", read_only=True)
    given_by_name = serializers.CharField(source="given_by.name", read_only=True, allow_null=True)

    class Meta:
        model = BlackMark
        fields = [
            "id",
            "team",
            "team_name",
            "reason",
            "penalty",
            "given_by",
            "given_by_name",
            "created_at",
        ]
        read_only_fields = ["given_by", "created_at"]


class BlackMarkListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка штрафов."""

    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = BlackMark
        fields = ["id", "team", "team_name", "reason", "penalty", "created_at"]
