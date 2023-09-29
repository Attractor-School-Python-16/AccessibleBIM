# Generated by Django 4.1.10 on 2023-09-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_alter_currencyratemodel_base_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyratemodel',
            name='base_currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='currencyratemodel',
            name='goal_currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], max_length=3, verbose_name='Валюта'),
        ),
    ]