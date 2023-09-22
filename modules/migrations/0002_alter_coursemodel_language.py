# Generated by Django 4.1.10 on 2023-09-22 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='language',
            field=models.CharField(choices=[('EN', 'Английский'), ('RU', 'Русский'), ('KG', 'Кыргызский')], max_length=10, verbose_name='Язык занятия'),
        ),
    ]
