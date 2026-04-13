from django.contrib import admin
from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'telegram_id', 'phone', 
                    'created_at')
    search_fields = ('name', 'telegram_id', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)