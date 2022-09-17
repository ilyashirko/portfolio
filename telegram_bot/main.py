import time
from logging import INFO, Logger
from textwrap import dedent

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from main.models import Visitor
from telegram_bot import messages

BUTTONS = {
    'biography': 'Краткая автобиография',
    'portfolio': 'Портфолио',
    'order_tg_bot': 'Заказать телеграм бота',
    'main': 'Вернуться на главную',
    'await': 'Загружаю данные...'
}


class TelegramBot():
    def __init__(self, **kwargs):
        self.telegram_bot_token = kwargs.get('telegram_bot_token', None)
        self.admin_telegram_id = kwargs.get('admin_telegram_id', None)
        self.updater = Updater(token=self.telegram_bot_token, use_context=True)

    class Keyboard():
        def __init__(self, **kwargs):
            self.header_buttons = kwargs.get('header_buttons', None)
            self.main_buttons = kwargs.get('main_buttons', None)
            self.footer_buttons = kwargs.get('footer_buttons', None)
            self.resize = kwargs.get('resize', True)
            self.one_time = kwargs.get('one_time', False)

        def make_keyboard(self):
            buttons = list()
            if self.header_buttons:
                buttons += self.header_buttons
            if self.main_buttons:
                buttons += self.main_buttons
            if self.footer_buttons:
                buttons += self.footer_buttons
            return ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=self.resize,
                one_time_keyboard=self.one_time
            )

        def main_keyboard(self):
            buttons = [
                [KeyboardButton(BUTTONS['biography'])],
                [KeyboardButton(BUTTONS['portfolio'])],
                [KeyboardButton(BUTTONS['order_tg_bot'])]
            ]
            return ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True,
            ) 

    def main(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text=messages.MAIN_MENU,
            reply_markup=self.Keyboard().main_keyboard())

    def biography(self, update, context):
        if update.message.text in messages.BIO.keys():
            context.bot.send_photo(
                update.effective_chat.id,
                photo=open(messages.BIO[update.message.text]['img'], 'rb'),
                caption=messages.BIO[update.message.text]['text']
            )

    def message_handler(self, update, context):
        user_id = update.effective_chat.id
        if update.message.text == BUTTONS['biography']:
            context.bot.send_message(
                user_id,
                text=dedent(
                    '''
                    Чтобы было удобнее читать, я разделил биографию на разные периоды.
                    Выберите внизу тот, который интересует вас больше всего.
                    '''
                ),
                reply_markup=self.Keyboard(
                    main_buttons=[[button] for button in messages.BIO.keys()],
                    footer_buttons=[['Вернуться на главную']]
                ).make_keyboard()
            )
            return 
        elif update.message.text in messages.BIO.keys():
            return self.biography(update, context)
        elif update.message.text == BUTTONS['portfolio']:
            pass
        elif update.message.text == BUTTONS['order_tg_bot']:
            pass
        elif update.message.text == BUTTONS['main']:
            return self.main(update, context)

        context.bot.send_message(user_id, text=update.message.text)

    def start(self, update, context):
        visitor_tg_id = update.effective_chat.id
        _, created = Visitor.objects.get_or_create(telegram_id=visitor_tg_id)
        if created:
            context.bot.send_message(
                chat_id=self.admin_telegram_id,
                text=f'New visitor: {visitor_tg_id} ({update.effective_chat.username})'
            )
        context.bot.send_message(visitor_tg_id, text=messages.HELLO_MESSAGE)
        time.sleep(5)
        context.bot.send_message(visitor_tg_id, text=messages.BOT_OPPORTUNITIES)
        time.sleep(5)
        context.bot.send_message(
            visitor_tg_id,
            text=messages.BOT_INSTRUCTIONS,
        )
        time.sleep(3)
        self.main(update, context)

    def run_bot(self):
        self.updater.dispatcher.add_handler(
            CommandHandler(command='start', callback=self.start)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler(command='main', callback=self.main)
        )
        
        self.updater.dispatcher.add_handler(
            MessageHandler(filters=Filters.all, callback=self.message_handler)
        )
        
        self.updater.start_polling()
        self.updater.idle()
