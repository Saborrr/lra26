from django.contrib import admin

from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "trainer", "score", "penalty", "total_score", "position", "created_at")
    list_filter = ("trainer",)
    search_fields = ("name", "trainer__name")
    readonly_fields = ("created_at", "updated_at", "total_score")
    ordering = ("-score",)

    def total_score(self, obj):
        return obj.total_score

    total_score.short_description = "Итоговый счёт"
