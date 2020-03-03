from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    reply_text = f'Ваш ID = {chat_id}\n{text}'
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    count = 0
    update.message.reply_text(
        text=f'У вас {count} сообщений',
    )


class RunBot(object):
    def handle(self, *args, **options):
        #
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TELEGRAM_TOKEN,
            base_url=getattr(settings, 'TELEGRAM_PROXY_URL', None),
        )
        print(bot.get_me())

        # обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        # Регистрируем обрабочики
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(CommandHandler('count', do_count))

        # Запускаем
        updater.start_polling()
        updater.idle()