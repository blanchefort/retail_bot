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
from telegram import ParseMode
from telegram import ReplyKeyboardMarkup

from .commands import Commands
from .search import Search
from .order import Order
from .catalog import Catalog

from webpanel.models.seller_bill import SellerBill
from webpanel.models.transporter_bill import Delivery

from telegram_bot.models import Messages

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

        # Каталог
        catalog = Catalog(updater=self.updater)

        # Поиск - самый последний
        search = Search(updater=self.updater)

        # Работа по расписанию
        j = self.updater.job_queue
        job_minute = j.run_repeating(self._timer_handler, interval=5, first=0)
        # Сообщения от администрации
        job_messages = j.run_repeating(
            self._system_messages_handler,
            interval=settings.TELEGRAM_SCHEDULE_TIME,
            first=0)

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

    def _timer_handler(self, context):
        """Отправляем сообщения по расписанию
        """
        # Отправляем счета от продавца
        bills = SellerBill.objects.filter(reseived_flag=0)
        for b in bills:
            message = f'Здравствуйте!\nВаш заказ №{b.order_number} обработан и выставлен счёт.'
            message += '\nДля того, чтобы заказ был доставлен, его необходимо оплатить.'

            context.bot.send_message(
                chat_id=b.user.profile.telegram_id,
                text=message,
                reply_markup=ReplyKeyboardMarkup(menu_kb()))
            context.bot.send_document(
                chat_id=b.user.profile.telegram_id,
                document=b.file_name.open(mode='rb'))

            message = 'Не забудьте проверить, указан ли ваш адрес для доставки!'
            message += '\n Сделать это можно с помощью команды /address'
            context.bot.send_message(
                chat_id=b.user.profile.telegram_id,
                text=message,
                reply_markup=ReplyKeyboardMarkup(menu_kb()))
            
            b.reseived_flag = 1
            b.save()
        
        # Отправляем стоимость доставки от транспортника
        bills = Delivery.objects.filter(reseived_flag=None)
        for b in bills:
            message = f'Здравствуйте! Ваш заказ №{b.order_number} принят службой доставки.'
            message += f'\nСтоимость доставки составит {b.amount}₸.'
            message += f'\nВ случае возникновения вопросов по доставке обращайтесь по телефону: '
            message += b.user.profile.phone

            sb = SellerBill.objects.get(order_number=b.order_number)

            context.bot.send_message(
                chat_id=sb.user.profile.telegram_id,
                text=message,
                reply_markup=ReplyKeyboardMarkup(menu_kb()))
            
            b.reseived_flag = 1
            b.save()


    def _system_messages_handler(self, context):
        """Отправляем сообщения от администрации сервера,
        """
        messages = Messages.objects.filter(reseived_flag=0)
        for m in messages:
            context.bot.send_message(
                chat_id=m.chat_id,
                text=m.message,
                parse_mode=ParseMode.MARKDOWN)
            m.reseived_flag = 1
            m.save()
