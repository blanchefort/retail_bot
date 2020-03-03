from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class PriceLists(models.Model):
    """Список прайс-листов, загруженных продавцами

    Args:
        file_name (string): Имя загруженного на сервер файла
        uploaded (datetime): время загрузки
        user (integer): пользователь, которому принадлежит файл
    """
    file_name = models.FileField(
        upload_to=settings.MEDIA_PRICELISTS_DIR,
        verbose_name='Файл прайса'
        )
    uploaded = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
        )
    user = models.ForeignKey(User,
        on_delete=models.PROTECT,
        related_name='user_pricelists',
        verbose_name='Продавец'
        )
    
    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Загруженный прайс-лист'
        verbose_name_plural = 'Загруженные прайс-листы'