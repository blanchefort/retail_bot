import os
import sys
from threading import Thread

from django.conf import settings
from telegram.utils.request import Request
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import DictPersistence
from telegram.ext import CommandHandler
from telegram.ext import Filters

from .commands import Commands
from .search import Search
from .order import Order

class StartBot(object):
    """Запуск бота
    """
    def __init__(self):
        pass


    def start_polling(self, *args, **options) -> (Request, Bot, Updater):
        """Запуск бота в режиме опроса сервера
        """
        self.persistence = DictPersistence()
        self.request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        self.bot = Bot(
            request=self.request,
            token=settings.TELEGRAM_TOKEN,
            base_url=getattr(settings, 'TELEGRAM_PROXY_URL', None),
        )
        self.updater = Updater(
            bot=self.bot,
            persistence=self.persistence,
            use_context=True,
        )

        print(self.bot.get_me())

        # Регистрируем обрабочики
        self._register_handlers()

        # Запускаем
        self.updater.start_polling()
        self.updater.idle()

        return self.request, self.bot, self.updater


    def _register_handlers(self) -> None:
        """Регистрируем обработчики событий
        """
        # Рестарт бота
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('r', self._restart, filters=Filters.user(username='@blanchefort')))

        # Команды
        commands = Commands(updater=self.updater)

        # Просмотр и отправка заказа
        order = Order(updater=self.updater)

        # Поиск - самый последний
        search = Search(updater=self.updater)

    def _restart(self, update, context):
        """Рестарт бота
        """
        update.message.reply_text('Bot is restarting...')
        Thread(target=self._stop_and_restart).start()

    def _stop_and_restart(self):
        """Gracefully stop the Updater and replace the current process with a new one
        https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#simple-way-of-restarting-the-bot
        """
        self.updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)