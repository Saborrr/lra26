"""Сериализаторы для квестов."""

from rest_framework import serializers

from .models import Quest


class QuestSerializer(serializers.ModelSerializer):
    """Сериализатор квеста."""

    class Meta:
        model = Quest
        fields = [
            "id",
            "title",
            "description",
            "max_points",
            "category",
            "order",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class QuestListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка квестов."""

    class Meta:
        model = Quest
        fields = ["id", "title", "max_points", "category", "order"]