from django.apps import AppConfig


class TeamsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.teams"
    verbose_name = "Команды"

    def ready(self):
        # Подключаем signals
        import apps.teams.signals  # noqa: F401
