from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class SellerBill(models.Model):
    """Счета, выставляемые продавцами покупателям

    Args:
        seller (User): продавец
        user (User): покупатель
        order_number (int): номер (идентификатор заказа). Равен Order.order_number
        file_name (string): Имя загруженного на сервер файла
        uploaded (datetime): время загрузки
        order_sum (int): Сумма заказа
    """

    seller = models.ForeignKey(User,
        on_delete=models.PROTECT,
        related_name='bill_seller',
        verbose_name='Продавец'
        )
    user = models.ForeignKey(User,
        on_delete=models.PROTECT,
        related_name='bill_user',
        verbose_name='Покупатель'
        )
    order_number = models.IntegerField(
        verbose_name='Номер заказа'
        )
    file_name = models.FileField(
        upload_to=settings.MEDIA_SELLERS_BILLS_DIR,
        verbose_name='Файл счёта'
        )
    uploaded = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
        )
    order_sum = models.FloatField(
        verbose_name='Сумма, тенге'
        )

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Загруженный cчёт на оплату товара'
        verbose_name_plural = 'Загруженные счета на оплату товара'
