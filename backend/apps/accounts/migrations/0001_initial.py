import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [(migrations.swappable_dependency(settings.AUTH_USER_MODEL))]

    operations = [
        migrations.CreateModel(
            name="AuditEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("action", models.CharField(max_length=100)),
                ("target_type", models.CharField(blank=True, max_length=100)),
                ("target_id", models.CharField(blank=True, max_length=100)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="LoginCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("code_hash", models.CharField(max_length=64, unique=True)),
                ("expires_at", models.DateTimeField()),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_login_codes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="login_codes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="PlatformIdentity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "provider",
                    models.CharField(
                        choices=[("telegram", "Telegram"), ("vk", "ВКонтакте")], max_length=16
                    ),
                ),
                ("external_id", models.CharField(max_length=64)),
                ("display_name", models.CharField(blank=True, max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_login_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="platform_identities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="platformidentity",
            constraint=models.UniqueConstraint(
                fields=("provider", "external_id"), name="unique_platform_identity"
            ),
        ),
        migrations.AddIndex(
            model_name="auditevent",
            index=models.Index(
                fields=["action", "created_at"], name="accounts_au_action_6cf40e_idx"
            ),
        ),
    ]
