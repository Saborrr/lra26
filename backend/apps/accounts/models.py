import hashlib
import hmac
import secrets

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone


class PlatformIdentity(models.Model):
    class Provider(models.TextChoices):
        TELEGRAM = "telegram", "Telegram"
        VK = "vk", "ВКонтакте"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="platform_identities",
    )
    provider = models.CharField(max_length=16, choices=Provider.choices)
    external_id = models.CharField(max_length=64)
    display_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "external_id"], name="unique_platform_identity"
            ),
            models.UniqueConstraint(
                fields=["user", "provider"], name="unique_user_platform_identity"
            ),
        ]

    def __str__(self):
        return f"{self.provider}:{self.external_id}"


class LoginCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_codes",
    )
    code_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_login_codes",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(used_at__isnull=True),
                name="one_unused_login_code_per_user",
            )
        ]

    @staticmethod
    def hash_code(code: str) -> str:
        return hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            code.strip().upper().encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @classmethod
    @transaction.atomic
    def issue(cls, *, user, created_by, lifetime_minutes: int = 15):
        type(user).objects.select_for_update().get(pk=user.pk)
        cls.objects.filter(user=user, used_at__isnull=True).delete()
        code = "-".join(
            [
                secrets.token_hex(2).upper(),
                secrets.token_hex(2).upper(),
                secrets.token_hex(2).upper(),
            ]
        )
        instance = cls.objects.create(
            user=user,
            created_by=created_by,
            code_hash=cls.hash_code(code),
            expires_at=timezone.now() + timezone.timedelta(minutes=lifetime_minutes),
        )
        return instance, code

    @property
    def is_valid(self):
        return self.used_at is None and self.expires_at > timezone.now()


class AuditEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_events",
    )
    action = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100, blank=True)
    target_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action", "created_at"], name="accounts_au_action_6cf40e_idx")
        ]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.action}"
