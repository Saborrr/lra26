from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import get_md5_hash_password

from .models import AuditEvent, LoginCode, PlatformIdentity
from .permissions import IsAdmin, IsSuperAdmin
from .serializers import (
    AuditEventSerializer,
    CurrentUserSerializer,
    LoginCodeSerializer,
    ParticipantDirectorySerializer,
    UserManagementSerializer,
)
from .services import (
    audit,
    resolve_platform_user,
    token_pair_for_user,
    validate_telegram_init_data,
    validate_vk_launch_params,
)

User = get_user_model()


class TrustedBrowserOriginMixin:
    def initial(self, request, *args, **kwargs):
        origin = request.headers.get("Origin")
        trusted = {item.rstrip("/") for item in settings.CSRF_TRUSTED_ORIGINS}
        trusted.add(settings.APP_PUBLIC_URL.rstrip("/"))
        if origin and origin.rstrip("/") not in trusted:
            raise PermissionDenied("Недоверенный источник запроса")
        return super().initial(request, *args, **kwargs)


def locked_refresh_token(raw):
    unchecked = RefreshToken(raw, verify=False)
    jti = unchecked.get(api_settings.JTI_CLAIM)
    if not jti:
        raise TokenError("Token has no id")
    OutstandingToken.objects.select_for_update().get(jti=jti)
    return RefreshToken(raw)


@transaction.atomic
def token_response(user, *, request, action_name):
    access, refresh = token_pair_for_user(user)
    audit(action=action_name, actor=user, request=request)
    response = Response({"access": access, "user": CurrentUserSerializer(user).data})
    response.set_cookie(
        settings.REFRESH_COOKIE_NAME,
        refresh,
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH,
    )
    return response


class LoginView(TrustedBrowserOriginMixin, APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        username = str(request.data.get("username", ""))[:150]
        password = str(request.data.get("password", ""))[:256]
        user = authenticate(request, username=username, password=password)
        if not user or not user.is_active:
            raise AuthenticationFailed("Неверный логин или пароль")
        return token_response(user, request=request, action_name="auth.login")


class RefreshView(TrustedBrowserOriginMixin, APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "refresh"

    @transaction.atomic
    def post(self, request):
        raw = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if not raw:
            raise AuthenticationFailed("Сессия отсутствует")
        try:
            old = locked_refresh_token(raw)
            user = User.objects.get(pk=old["user_id"], is_active=True)
            if old.get(api_settings.REVOKE_TOKEN_CLAIM) != get_md5_hash_password(user.password):
                raise TokenError("Password changed")
            old.blacklist()
        except (TokenError, OutstandingToken.DoesNotExist, User.DoesNotExist, KeyError) as exc:
            raise AuthenticationFailed("Сессия истекла") from exc
        return token_response(user, request=request, action_name="auth.refresh")


class LogoutView(TrustedBrowserOriginMixin, APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        raw = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if raw:
            try:
                locked_refresh_token(raw).blacklist()
            except (TokenError, OutstandingToken.DoesNotExist):
                pass
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.REFRESH_COOKIE_NAME, path=settings.REFRESH_COOKIE_PATH)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(CurrentUserSerializer(request.user).data)


class ParticipantDirectoryView(APIView):
    """Minimal account directory used to attach participant profiles."""

    permission_classes = [IsAdmin]

    def get(self, request):
        users = (
            User.objects.filter(is_staff=False, is_superuser=False)
            .select_related("trainer")
            .order_by("username")
        )
        return Response(ParticipantDirectorySerializer(users, many=True).data)


class TelegramAuthView(TrustedBrowserOriginMixin, APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "platform_auth"

    def post(self, request):
        data = validate_telegram_init_data(str(request.data.get("init_data", "")))
        user = resolve_platform_user(
            provider=PlatformIdentity.Provider.TELEGRAM,
            link_code=str(request.data.get("link_code", "")),
            **data,
        )
        return token_response(user, request=request, action_name="auth.telegram")


class VkAuthView(TrustedBrowserOriginMixin, APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "platform_auth"

    def post(self, request):
        data = validate_vk_launch_params(str(request.data.get("launch_params", "")))
        user = resolve_platform_user(
            provider=PlatformIdentity.Provider.VK,
            link_code=str(request.data.get("link_code", "")),
            **data,
        )
        return token_response(user, request=request, action_name="auth.vk")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False).order_by("username")
    serializer_class = UserManagementSerializer
    permission_classes = [IsSuperAdmin]
    http_method_names = ["get", "post", "patch", "head", "options"]

    @transaction.atomic
    def perform_create(self, serializer):
        user = serializer.save()
        audit(action="user.create", actor=self.request.user, target=user, request=self.request)

    @transaction.atomic
    def perform_update(self, serializer):
        if serializer.instance == self.request.user:
            raise PermissionDenied("Нельзя изменить собственные права через этот интерфейс")
        user = serializer.save()
        audit(action="user.update", actor=self.request.user, target=user, request=self.request)


class LoginCodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginCodeSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return LoginCode.objects.select_related("user").all()

    @action(detail=False, methods=["post"])
    def issue(self, request):
        try:
            user = User.objects.get(pk=request.data.get("user"), is_active=True)
        except User.DoesNotExist as exc:
            raise PermissionDenied("Пользователь не найден") from exc
        if user.is_staff and not request.user.is_superuser:
            raise PermissionDenied("Коды администраторов выдаёт только суперадминистратор")
        instance, plain_code = LoginCode.issue(user=user, created_by=request.user)
        data = LoginCodeSerializer(instance).data
        data["code"] = plain_code
        audit(action="login_code.issue", actor=request.user, target=user, request=request)
        return Response(data, status=status.HTTP_201_CREATED)


class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditEvent.objects.select_related("actor").all()
    serializer_class = AuditEventSerializer
    permission_classes = [IsSuperAdmin]
