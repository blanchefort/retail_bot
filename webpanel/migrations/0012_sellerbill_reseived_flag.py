# Generated by Django 3.0.3 on 2020-03-15 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0011_sellerbill'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerbill',
            name='reseived_flag',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Отметка о получении счёта покупателем'),
        ),
    ]