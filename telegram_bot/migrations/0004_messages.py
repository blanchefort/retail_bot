# Generated by Django 3.0.3 on 2020-03-19 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegram_bot', '0003_auto_20200317_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время запроса')),
                ('chat_id', models.IntegerField(default=0, null=True, verbose_name='Идентификатор чата в ТГ')),
                ('message', models.TextField(default=None, null=True, verbose_name='Текст сообщения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_to_telegram_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сообщение администрации сайта',
                'verbose_name_plural': 'Сообщения администрации сайта',
            },
        ),
    ]