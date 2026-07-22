from rest_framework import serializers

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source="trainer.name", read_only=True)
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
            "total_score",
            "position",
            "color",
            "logo",
        ]
        read_only_fields = ["score", "penalty", "total_score", "position"]


class TeamListSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source="trainer.name", read_only=True)
    total_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "trainer_name", "score", "penalty", "total_score", "color", "logo"]


class TeamLeaderboardSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source="trainer.name", read_only=True)
    total_score = serializers.IntegerField(read_only=True)
    position = serializers.SerializerMethodField()

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
            "logo",
            "position",
        ]

    def get_position(self, obj):
        return getattr(obj, "leaderboard_position", obj.position)
