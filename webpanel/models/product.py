from django.db import models
from django.contrib.auth.models import User
from .product_category import ProductCategory
from .product_unit_type import ProductUnitType


class Product(models.Model):
    """Товары

    Args:
        title (string): Название товара
        category (string): Категория товара
        user (integer): Пользователь, добавивший товар
        unit (integer): Единица измерения товара
        price (float): Цена товара
        is_active (bool): отметка о том, активен ли товар. True - активен.
    """
    title = models.TextField(verbose_name='Наименование', db_index=True)
    category = models.ForeignKey(ProductCategory,
        null=True,
        on_delete=models.PROTECT,
        related_name='category_products',
        verbose_name='Категория'
        )
    user = models.ForeignKey(User,
        on_delete=models.PROTECT,
        related_name='user_products',
        verbose_name='Пользователь'
        )
    unit = models.ForeignKey(
        ProductUnitType,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Ед. изм.'
        )
    price = models.FloatField(verbose_name='Цена, тенге', default=0.0)
    is_active = models.BooleanField(verbose_name='Активность', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'