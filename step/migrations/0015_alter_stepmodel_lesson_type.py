# Generated by Django 4.1.10 on 2023-09-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step', '0014_stepmodel_serial_number_alter_stepmodel_chapter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepmodel',
            name='lesson_type',
            field=models.CharField(choices=[('test', 'Тест'), ('video', 'Видео'), ('text', 'Текст')], max_length=10, verbose_name='Тип занятия'),
        ),
    ]
