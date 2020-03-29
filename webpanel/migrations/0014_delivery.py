# Generated by Django 3.0.3 on 2020-03-16 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webpanel', '0013_auto_20200316_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(default=0, null=True, verbose_name='Номер заказа')),
                ('amount', models.FloatField(default=0.0, verbose_name='сумма транспортных услуг')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transporter_delivery', to=settings.AUTH_USER_MODEL, verbose_name='транспортник, который исполняет заказ')),
            ],
            options={
                'verbose_name': 'Заказ на доставку',
                'verbose_name_plural': 'Заказы на доставку',
            },
        ),
    ]