from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('team', 'quest', 'points', 'verified', 
                    'entered_by', 'timestamp')
    list_filter = ('verified', 'quest', 'team')
    search_fields = ('team__name', 'quest__title')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)