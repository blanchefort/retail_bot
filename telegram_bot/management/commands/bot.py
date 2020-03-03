from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


from telegram_bot.bot.test import RunBot
from telegram_bot.bot.start import StartBot

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot_instance = StartBot()

        request, bot, updater = bot_instance.start_polling()