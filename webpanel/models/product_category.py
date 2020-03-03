from django.db import models


class ProductCategory(models.Model):
    """Категории товаров

    Args:
        name (string): Название категории
    """
    name = models.CharField(
        max_length=500,
        verbose_name='Название категории',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'