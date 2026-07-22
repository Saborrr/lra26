from django.contrib import admin

from .models import Quest


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "points", "category", "order", "active", "created_at")
    list_filter = ("active", "category")
    search_fields = ("id", "title", "description")
    readonly_fields = ("created_at",)
    ordering = ("order", "id")
