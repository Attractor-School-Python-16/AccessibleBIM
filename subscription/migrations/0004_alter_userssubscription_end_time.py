# Generated by Django 4.1.10 on 2023-09-22 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_alter_userssubscription_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userssubscription',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 20, 29, 22, 405801), verbose_name='Дата окончания подписки'),
        ),
    ]
