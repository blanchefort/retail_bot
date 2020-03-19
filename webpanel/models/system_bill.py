from django.db import models
from django.contrib.auth.models import User


class SystemBill(models.Model):
    """Счета, выставляемые системой пользователям: 
    продавцам, транспортинкам, покупателям.

    Args:
        user (User)             - пользователь
        date_start (datetime)   - начало действия оплаченного периода
        date_end    (datetime)  - конец действия оплаченного периода
        amount (float)          - оплаченная сумма
        actor (User)            - менеджер, активировавший данный период
    """
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_bill',
        verbose_name='Пользователь'
        )
    date_start = models.DateTimeField(
        verbose_name='Начало платного периода',
        default=None,
        null=True
        )
    date_end = models.DateTimeField(
        verbose_name='Окончание периода',
        default=None,
        null=True
        )
    amount = models.FloatField(
        verbose_name='Оплаченная сумма',
        default=0.0
        )
    actor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='manager_bill',
        verbose_name='Менеджер'
        )

    class Meta:
        verbose_name = 'Оплаченный аккаунт'
        verbose_name_plural = 'оплаченные аккаунты'