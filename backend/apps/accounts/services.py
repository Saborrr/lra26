import base64
import hashlib
import hmac
import ipaddress
import json
import time
from urllib.parse import parse_qsl

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuditEvent, LoginCode, PlatformIdentity


def get_client_ip(request):
    forwarded = [
        item.strip()
        for item in request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")
        if item.strip()
    ]
    proxy_count = settings.REST_FRAMEWORK.get("NUM_PROXIES", 0)
    candidate = (
        forwarded[-min(proxy_count, len(forwarded))]
        if forwarded and proxy_count > 0
        else request.META.get("REMOTE_ADDR")
    )
    try:
        return str(ipaddress.ip_address(candidate)) if candidate else None
    except ValueError:
        return None


def audit(*, action, actor=None, target=None, request=None, metadata=None):
    AuditEvent.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        action=action,
        target_type=target.__class__.__name__ if target else "",
        target_id=str(getattr(target, "pk", "")) if target else "",
        ip_address=get_client_ip(request) if request else None,
        metadata=metadata or {},
    )


def token_pair_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user_role(user)
    return str(refresh.access_token), str(refresh)


def user_role(user):
    if user.is_superuser:
        return "superadmin"
    if user.is_staff:
        return "admin"
    return "participant"


def validate_telegram_init_data(raw_data: str) -> dict:
    if not settings.TELEGRAM_BOT_TOKEN:
        raise AuthenticationFailed("Telegram integration is not configured")
    values = dict(parse_qsl(raw_data, keep_blank_values=True))
    received_hash = values.pop("hash", "")
    if not received_hash:
        raise AuthenticationFailed("Telegram signature is missing")
    try:
        auth_date = int(values.get("auth_date", "0"))
    except ValueError as exc:
        raise AuthenticationFailed("Invalid Telegram authorization date") from exc
    if abs(time.time() - auth_date) > settings.PLATFORM_AUTH_MAX_AGE_SECONDS:
        raise AuthenticationFailed("Telegram authorization data has expired")
    data_check_string = "\n".join(f"{key}={values[key]}" for key in sorted(values))
    secret = hmac.new(b"WebAppData", settings.TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    expected = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        raise AuthenticationFailed("Invalid Telegram signature")
    try:
        user_data = json.loads(values["user"])
        external_id = str(user_data["id"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise AuthenticationFailed("Telegram user data is missing") from exc
    return {
        "external_id": external_id,
        "display_name": " ".join(
            part for part in [user_data.get("first_name"), user_data.get("last_name")] if part
        ),
    }


def validate_vk_launch_params(raw_query: str) -> dict:
    if not settings.VK_APP_SECRET:
        raise AuthenticationFailed("VK integration is not configured")
    values = dict(parse_qsl(raw_query.lstrip("?"), keep_blank_values=True))
    received_sign = values.get("sign", "")
    signed = "&".join(f"{key}={values[key]}" for key in sorted(values) if key.startswith("vk_"))
    digest = hmac.new(settings.VK_APP_SECRET.encode(), signed.encode(), hashlib.sha256).digest()
    expected = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    if not received_sign or not hmac.compare_digest(expected, received_sign):
        raise AuthenticationFailed("Invalid VK signature")
    external_id = values.get("vk_user_id")
    if not external_id:
        raise AuthenticationFailed("VK user id is missing")
    try:
        timestamp = int(values["vk_ts"])
    except (KeyError, ValueError) as exc:
        raise AuthenticationFailed("Invalid VK authorization date") from exc
    if abs(time.time() - timestamp) > settings.PLATFORM_AUTH_MAX_AGE_SECONDS:
        raise AuthenticationFailed("VK authorization data has expired")
    return {"external_id": external_id, "display_name": ""}


@transaction.atomic
def resolve_platform_user(*, provider, external_id, display_name="", link_code=""):
    identity = (
        PlatformIdentity.objects.select_for_update()
        .select_related("user")
        .filter(provider=provider, external_id=external_id)
        .first()
    )
    if identity:
        if not identity.user.is_active:
            raise AuthenticationFailed("User account is disabled")
        identity.display_name = display_name or identity.display_name
        identity.last_login_at = timezone.now()
        identity.save(update_fields=["display_name", "last_login_at"])
        return identity.user

    if not link_code:
        raise ValidationError({"link_code": "Для первой привязки нужен одноразовый код"})

    code = (
        LoginCode.objects.select_for_update()
        .select_related("user")
        .filter(code_hash=LoginCode.hash_code(link_code))
        .first()
    )
    if not code or not code.is_valid:
        raise ValidationError({"link_code": "Код недействителен или уже использован"})
    if not code.user.is_active:
        raise AuthenticationFailed("User account is disabled")
    PlatformIdentity.objects.create(
        user=code.user,
        provider=provider,
        external_id=external_id,
        display_name=display_name,
        last_login_at=timezone.now(),
    )
    code.used_at = timezone.now()
    code.save(update_fields=["used_at"])
    if provider == PlatformIdentity.Provider.TELEGRAM and hasattr(code.user, "trainer"):
        code.user.trainer.telegram_id = int(external_id)
        code.user.trainer.save(update_fields=["telegram_id", "updated_at"])
    return code.user
