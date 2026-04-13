from django.contrib import admin
from .models import BlackMark


@admin.register(BlackMark)
class BlackMarkAdmin(admin.ModelAdmin):
    list_display = ('team', 'reason', 'penalty', 'given_by', 
                    'created_at')
    list_filter = ('team', 'given_by')
    search_fields = ('team__name', 'reason')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)