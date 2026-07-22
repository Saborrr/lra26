from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the LRA-26 Telegram bot in long-polling mode"

    def handle(self, *args, **options):
        from bot.handlers import create_application

        self.stdout.write(self.style.SUCCESS("Telegram bot started"))
        create_application().run_polling(
            allowed_updates=["message", "callback_query"], drop_pending_updates=False
        )
