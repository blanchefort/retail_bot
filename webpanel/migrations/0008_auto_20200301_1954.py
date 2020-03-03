# Generated by Django 3.0.3 on 2020-03-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0007_order_product_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bill_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='Время выставления счёта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='Время принятия заявки транспортником'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Номер заказа'),
        ),
    ]
