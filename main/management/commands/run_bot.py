from django.core.management.base import BaseCommand
from telegram_bot.main import TelegramBot
from environs import Env

class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        env = Env()
        env.read_env()

        bot = TelegramBot(
            telegram_bot_token=env.str('TELEGRAM_BOT_TOKEN'),
            admin_telegram_id=env.int('ADMIN_TELEGRAM_ID')
        )
        bot.run_bot()
