# Generated by Django 3.0.3 on 2020-03-01 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_count',
            field=models.FloatField(default=0.0, verbose_name='Стоимость, тенге'),
        ),
    ]