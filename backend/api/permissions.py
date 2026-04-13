"""Кастомные permissions для API."""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает чтение всем, запись только админам."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsTeamTrainer(permissions.BasePermission):
    """Разрешает запись только тренеру команды."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # Получаем тренера пользователя
        try:
            trainer = request.user.trainer
        except AttributeError:
            return False
        # Проверяем, что объект связан с командой тренера
        if hasattr(obj, "team"):
            return obj.team.trainer == trainer
        if hasattr(obj, "trainer"):
            return obj.trainer == trainer
        return False


class IsSuperAdmin(permissions.BasePermission):
    """Разрешает доступ только суперпользователям."""

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser