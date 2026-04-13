"""Сериализаторы для тренеров."""

from rest_framework import serializers

from .models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    """Полный сериализатор тренера."""

    teams_count = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "id",
            "user",
            "name",
            "telegram_id",
            "phone",
            "teams_count",
        ]
        read_only_fields = ["user"]

    def get_teams_count(self, obj):
        """Возвращает количество команд тренера."""
        return obj.teams.count()


class TrainerListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка тренеров."""

    class Meta:
        model = Trainer
        fields = ["id", "name", "telegram_id"]


class TrainerCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания тренера."""

    class Meta:
        model = Trainer
        fields = ["name", "telegram_id", "phone"]