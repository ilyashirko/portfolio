import time
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from main.models import Visitor
from logging import INFO, Logger

from telegram_bot.messages import BOT_OPPORTUNITIES, HELLO_MESSAGE, BOT_INSTRUCTIONS

class TelegramBot():
    def __init__(self, **kwargs):
        self.telegram_bot_token = kwargs.get('telegram_bot_token', None)
        self.admin_telegram_id = kwargs.get('admin_telegram_id', None)
        self.updater = Updater(token=self.telegram_bot_token, use_context=True)

    class Keyboard():
        pass

    def echo(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text
        )

    def message_handler(self, update, context):
        return self.echo(update, context)

    def start(self, update, context):
        visitor_tg_id = update.effective_chat.id
        _, created = Visitor.objects.get_or_create(telegram_id=visitor_tg_id)
        if created:
            context.bot.send_message(
                chat_id=self.admin_telegram_id,
                text=f'New visitor: {visitor_tg_id} ({update.effective_chat.username})'
            )
        context.bot.send_message(visitor_tg_id, text=HELLO_MESSAGE)
        time.sleep(5)
        context.bot.send_message(visitor_tg_id, text=BOT_OPPORTUNITIES)
        time.sleep(5)
        context.bot.send_message(visitor_tg_id, text=BOT_INSTRUCTIONS)

    def run_bot(self):
        self.updater.dispatcher.add_handler(
            CommandHandler(command='start', callback=self.start)
        )
        self.updater.dispatcher.add_handler(
            MessageHandler(filters=Filters.all, callback=self.message_handler)
        )
        self.updater.start_polling()
        self.updater.idle()