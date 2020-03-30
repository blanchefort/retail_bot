from django.db import models


class ProductUnitType(models.Model):
    """Единицы измерения товара

    Args:
        name (string): название единицы измерения
        short (string): Краткое наименование
    """
    name = models.CharField(
        max_length=20,
        verbose_name='Наименование ед. изм.',
        default='ед.изм.',
        null=True
    )
    short = models.CharField(
        max_length=10,
        verbose_name='Краткое наименование',
        default='ед.изм.',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'