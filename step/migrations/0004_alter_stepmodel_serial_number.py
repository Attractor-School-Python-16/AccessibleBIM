# Generated by Django 4.1.10 on 2023-09-24 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step', '0003_merge_20230924_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepmodel',
            name='serial_number',
            field=models.PositiveIntegerField(),
        ),
    ]
