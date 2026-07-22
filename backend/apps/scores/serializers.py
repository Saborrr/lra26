from rest_framework import serializers

from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)
    quest_title = serializers.CharField(source="quest.title", read_only=True)
    entered_by_name = serializers.CharField(source="entered_by.name", read_only=True)

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
            "entered_by_name",
            "notes",
            "timestamp",
            "updated_at",
        ]
        read_only_fields = ["entered_by_name", "timestamp", "updated_at"]
        # The API intentionally treats a repeated team/quest pair as an update.
        # Database uniqueness still provides the final integrity guarantee.
        validators = []

    def validate(self, attrs):
        quest = attrs.get("quest") or getattr(self.instance, "quest", None)
        points = attrs.get("points", getattr(self.instance, "points", 0))
        if quest and points > quest.points:
            raise serializers.ValidationError({"points": f"Максимум для задания: {quest.points}"})
        return attrs
