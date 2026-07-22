from rest_framework import serializers

from .models import Quest


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = [
            "id",
            "title",
            "description",
            "points",
            "category",
            "order",
            "active",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_id(self, value):
        if not value.replace("-", "").replace("_", "").isalnum():
            raise serializers.ValidationError("ID может содержать буквы, цифры, - и _")
        return value


class QuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ["id", "title", "description", "points", "category", "order", "active"]
