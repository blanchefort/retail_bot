from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Профиль пользователя

    Args:
        type (integer): тип пользователя
        company_name (string): название организации
        address (string): юридический адрес
        bin (integer): Бизнес-идентификационный номер
        bank_account (string): банковские реквизиты
        phone (string): телефонный номер
        telegram_id (integer): Идентификатор в Телеграме
    """
    USER_TYPES = [
        (5, 'Менеджер сервиса'),
        (4, 'Продавец'),
        (3, 'Транспортник'),
        (2, 'Платный пользователь'),
        (1, 'Бесплатный пользователь'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.IntegerField(choices=USER_TYPES, default=5, verbose_name='Тип')
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        default=None,
        blank=True,
        null=True
    )
    company_name = models.CharField(
        max_length=1500,
        verbose_name='Название компании',
        default=None,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=1500,
        verbose_name='Юридический адрес',
        default=None,
        blank=True,
        null=True
    )
    bin = models.IntegerField(verbose_name='БИН', default=None, blank=True, null=True)
    bank_account = models.CharField(
        max_length=1500,
        verbose_name='Банковские реквизиты',
        default=None,
        blank=True,
        null=True
    )

    telegram_id = models.IntegerField(
        verbose_name='Телеграм-идентификатор пользователя',
        default=None,
        blank=True,
        null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
