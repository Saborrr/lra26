from rest_framework import serializers

from .models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    teams_count = serializers.IntegerField(source="teams.count", read_only=True)

    class Meta:
        model = Trainer
        fields = ["id", "user", "username", "name", "telegram_id", "phone", "teams_count"]


class TrainerListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Trainer
        fields = ["id", "user", "username", "name", "telegram_id", "teams_count"]

    teams_count = serializers.IntegerField(source="teams.count", read_only=True)


class TrainerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ["user", "name", "telegram_id", "phone"]

    def validate_user(self, user):
        if not user.is_active:
            raise serializers.ValidationError("Пользователь отключён")
        if user.is_staff or user.is_superuser:
            raise serializers.ValidationError("Профиль участника нельзя связать с администратором")
        return user
