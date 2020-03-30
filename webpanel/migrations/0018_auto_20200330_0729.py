# Generated by Django 3.0.3 on 2020-03-30 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0017_systembill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productunittype',
            name='name',
            field=models.CharField(default='ед.изм.', max_length=20, null=True, verbose_name='Наименование ед. изм.'),
        ),
        migrations.AlterField(
            model_name='productunittype',
            name='short',
            field=models.CharField(default='ед.изм.', max_length=10, null=True, verbose_name='Краткое наименование'),
        ),
    ]