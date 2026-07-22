import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.test import APIClient

from apps.accounts.models import LoginCode, PlatformIdentity
from apps.accounts.services import validate_telegram_init_data

User = get_user_model()


@pytest.mark.django_db
def test_password_login_refresh_and_logout():
    User.objects.create_user(username="participant", password="a-very-long-test-password")
    client = APIClient()
    login = client.post(
        "/api/auth/login/",
        {"username": "participant", "password": "a-very-long-test-password"},
        format="json",
    )
    assert login.status_code == 200
    assert login.data["user"]["role"] == "participant"
    assert "lra26_refresh" in login.cookies

    refresh = client.post("/api/auth/refresh/", {}, format="json")
    assert refresh.status_code == 200
    assert refresh.data["access"]

    logout = client.post("/api/auth/logout/", {}, format="json")
    assert logout.status_code == 204


@pytest.mark.django_db
def test_browser_auth_rejects_untrusted_origin():
    User.objects.create_user(username="participant", password="a-very-long-test-password")
    client = APIClient()
    response = client.post(
        "/api/auth/login/",
        {"username": "participant", "password": "a-very-long-test-password"},
        format="json",
        HTTP_ORIGIN="https://evil.example",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_issuing_new_link_code_revokes_previous_code():
    admin = User.objects.create_superuser(username="root", password="a-very-long-test-password")
    participant = User.objects.create_user(username="crew")
    first, _ = LoginCode.issue(user=participant, created_by=admin)
    second, _ = LoginCode.issue(user=participant, created_by=admin)
    assert not LoginCode.objects.filter(pk=first.pk).exists()
    assert LoginCode.objects.filter(pk=second.pk, used_at__isnull=True).count() == 1


@pytest.mark.django_db
def test_login_code_is_single_use():
    admin = User.objects.create_superuser(username="root", password="a-very-long-test-password")
    participant = User.objects.create_user(username="crew")
    _, plain_code = LoginCode.issue(user=participant, created_by=admin)

    from apps.accounts.services import resolve_platform_user

    linked = resolve_platform_user(
        provider=PlatformIdentity.Provider.TELEGRAM,
        external_id="12345",
        display_name="Crew Member",
        link_code=plain_code,
    )
    assert linked == participant
    assert PlatformIdentity.objects.filter(external_id="12345").exists()

    with pytest.raises(ValidationError):
        resolve_platform_user(
            provider=PlatformIdentity.Provider.VK,
            external_id="77",
            link_code=plain_code,
        )


@override_settings(TELEGRAM_BOT_TOKEN="123:test-token", PLATFORM_AUTH_MAX_AGE_SECONDS=600)
def test_telegram_signature_is_verified():
    values = {
        "auth_date": str(int(time.time())),
        "query_id": "AAE-test",
        "user": json.dumps({"id": 42, "first_name": "Alex"}, separators=(",", ":")),
    }
    check = "\n".join(f"{key}={values[key]}" for key in sorted(values))
    secret = hmac.new(b"WebAppData", b"123:test-token", hashlib.sha256).digest()
    values["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    result = validate_telegram_init_data(urlencode(values))
    assert result == {"external_id": "42", "display_name": "Alex"}

    values["hash"] = "0" * 64
    with pytest.raises(AuthenticationFailed):
        validate_telegram_init_data(urlencode(values))


@pytest.mark.django_db
def test_expired_link_code_is_rejected():
    participant = User.objects.create_user(username="expired")
    instance, plain_code = LoginCode.issue(user=participant, created_by=None)
    instance.expires_at = timezone.now() - timezone.timedelta(seconds=1)
    instance.save(update_fields=["expires_at"])
    assert not instance.is_valid

    from apps.accounts.services import resolve_platform_user

    with pytest.raises(ValidationError):
        resolve_platform_user(
            provider=PlatformIdentity.Provider.TELEGRAM,
            external_id="987",
            link_code=plain_code,
        )
