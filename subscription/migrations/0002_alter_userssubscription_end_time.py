# Generated by Django 4.1.10 on 2023-09-22 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userssubscription',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 20, 26, 36, 76254), verbose_name='Дата окончания подписки'),
        ),
    ]
