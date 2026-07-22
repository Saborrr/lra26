from django.contrib import admin

from .models import AuditEvent, LoginCode, PlatformIdentity


@admin.register(PlatformIdentity)
class PlatformIdentityAdmin(admin.ModelAdmin):
    list_display = ("provider", "external_id", "user", "last_login_at")
    search_fields = ("external_id", "user__username")
    readonly_fields = ("created_at", "last_login_at")


@admin.register(LoginCode)
class LoginCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "used_at", "created_by")
    readonly_fields = ("code_hash", "created_at", "used_at")


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "actor", "target_type", "target_id")
    list_filter = ("action", "target_type")
    readonly_fields = [field.name for field in AuditEvent._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
