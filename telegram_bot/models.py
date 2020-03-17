from django.db import models
from django.contrib.auth.models import User

class Logger(models.Model):
    """Логирование в БД всех пользовательских запросов,
    приходящих из Телеграма.

    Структура таблицы:
        datetime (datetime) - время запроса
        user (User)         - объект пользователя в системе
        chat_id (int)       - идентификатор чата
        message (str)       - сообщение от пользователя
    """
    datetime = models.DateTimeField(
        verbose_name='Время запроса',
        auto_now_add=True
        )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='telegram_message',
        verbose_name='Пользователь'
        )
    chat_id = models.IntegerField(
        verbose_name='Идентификатор чата в ТГ',
        default=0,
        null=True
        )
    message = models.TextField(
        verbose_name='Текст запроса',
        default=None,
        null=True
    )

    def __str__(self):
        return str(self.message)

    class Meta:
        verbose_name = 'Запрос из Телеграма'
        verbose_name_plural = 'Запросы из Телеграма'