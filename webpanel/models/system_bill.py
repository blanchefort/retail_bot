from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
import pytz


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


def check_user_type(user):
    """Проверка типа пользователя.
    Если у пользователя активирован платный период, выставляется 
    profile.type = 2.
    Если платный период истёк, выставляется 
    profile.type = 1
    """
    utc=pytz.UTC

    if SystemBill.objects.filter(user=user):
        last_payment = SystemBill.objects.filter(user=user).last()

        date_end = last_payment.date_end.replace(tzinfo=utc)
        date_now = datetime.now().replace(tzinfo=utc)

        if date_end > date_now:
            # Окончание периода не наступило, значит - тип 2
            user.profile.type = 2
            user.save()
        elif date_end < date_now:
            # Период закончился, выставляем тип 1
            user.profile.type = 1
            user.save()
    else:
        user.profile.type = 1
        user.save()