from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import AuditEvent, LoginCode, PlatformIdentity
from .services import user_role

User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    trainer_id = serializers.IntegerField(source="trainer.id", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "role", "trainer_id"]

    def get_role(self, obj):
        return user_role(obj)


class ParticipantDirectorySerializer(serializers.ModelSerializer):
    trainer_id = serializers.IntegerField(source="trainer.id", read_only=True, allow_null=True)
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "display_name", "trainer_id", "is_active"]
        read_only_fields = fields

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username


class UserManagementSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=["participant", "admin"], write_only=True, required=False
    )
    current_role = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, min_length=12)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "role",
            "current_role",
            "password",
        ]
        read_only_fields = ["current_role"]

    def get_current_role(self, obj):
        return user_role(obj)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", "participant")
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError({"password": "Пароль обязателен"})
        user = User(**validated_data, is_staff=role == "admin")
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        role = validated_data.pop("role", None)
        password = validated_data.pop("password", None)
        if role:
            instance.is_staff = role == "admin"
        password_changed = bool(password)
        if password_changed:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        if password_changed:
            for token in OutstandingToken.objects.filter(user=instance):
                BlacklistedToken.objects.get_or_create(token=token)
        return instance


class PlatformIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformIdentity
        fields = ["id", "provider", "external_id", "display_name", "last_login_at"]
        read_only_fields = fields


class LoginCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = LoginCode
        fields = ["id", "user", "username", "code", "expires_at", "used_at", "created_at"]
        read_only_fields = ["expires_at", "used_at", "created_at"]


class AuditEventSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = AuditEvent
        fields = [
            "id",
            "actor_name",
            "action",
            "target_type",
            "target_id",
            "metadata",
            "created_at",
        ]
        read_only_fields = fields
