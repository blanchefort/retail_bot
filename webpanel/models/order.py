from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Order(models.Model):
    """Заказы

    Args:
        product (Product): идентификатор товара
        user (User): идентификатор пользователя
        product_count (float): Количество заказанного товара. Если выставлен ноль, значит пользователь 
            только добавил товар в корзину, но ещё не оформил до конца заявку.
        creation_date (datetime): дата создания пользователем заявки
        bill_date (datetime): время выставления счёта продавцом (т.е. продавец увидел и обратал заявку).
        delivery_date (datetime): время принятия заявки транспортников 
            (т.е. пользователь сформировал заявку, потом продавец её оформил и выставил счёт,
            после выставления счёта, он уходит покупателю, все товары выбранной для счёта группы объединяются
            под единым идентификатором, и сформированный список становится доступен транспортникам).
        order_number (integer): номер заказа, формируется после того, как покупатель отправил сформированный
        заказ на обработку. Номер заказа может быть и у нескольких продавцов.
        status (integer): Статус заявки:
            0 - не сформирован, 
            1 - отправлен продавцу
            2 - продавец обработал, выставил счёт
            3 - транспортник принял к исполнению
            4 - продавец отметил, что заказ оплачен
            5 - удалён покупателем (удалить можно только с уровня 0, т.е. удаление из корзины,
            пока не был передан продавцу).
            6 - транспортник отметил, что заказ доставлен
            7 - транспортник отметил, что заказ оплачен
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='product_orders',
        verbose_name='Заказанный товар'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_orders',
        verbose_name='Пользователь, заказавший товар'
        )
    product_count = models.FloatField(
        verbose_name='Количество заказанного товара',
        default=0.0
        )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания заявки'
        )
    bill_date = models.DateTimeField(
        verbose_name='Время выставления счёта',
        default=None,
        null=True
        )
    delivery_date = models.DateTimeField(
        verbose_name='Время принятия заявки транспортником',
        default=None,
        null=True
        )
    order_number = models.IntegerField(
        verbose_name='Номер заказа',
        default=0,
        null=True
        )
    status = models.IntegerField(
        verbose_name='Статус заказа',
        default=0,
        null=True
    )

    def __str__(self):
        return str(self.product.title)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'