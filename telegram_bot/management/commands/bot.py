from django.core.management.base import BaseCommand

from telegram_bot.bot.start import StartBot

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot_instance = StartBot()

        request, bot, updater = bot_instance.start_polling()