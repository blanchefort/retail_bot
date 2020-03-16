"""Счета, выставляемые транспортниками за свои услуги
"""
from django.db import models
from django.contrib.auth.models import User


class Delivery(models.Model):
    """Данные по доставке

    Args:
        user (User) - транспортник, который исполняет заказ
        order_number (int) - номер заказа, Order.order_number
        amount (float) - сумма транспортных услуг
    """
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='transporter_delivery',
        verbose_name='транспортник, который исполняет заказ'
        )
    order_number = models.IntegerField(
        verbose_name='Номер заказа',
        default=0,
        null=True
        )
    amount = models.FloatField(
        verbose_name='сумма транспортных услуг',
        default=0.0
        )

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name = 'Заказ на доставку'
        verbose_name_plural = 'Заказы на доставку'