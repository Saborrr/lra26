"""Management command для запуска Telegram-бота."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Запускает Telegram-бота."""

    help = "Запускает Telegram-бота для LRA-26"

    def handle(self, *args, **options):
        """Запуск бота."""
        from bot.handlers import create_application

        self.stdout.write("Запуск Telegram-бота...")
        app = create_application()
        app.run_polling(allowed_updates=["message", "callback_query"])