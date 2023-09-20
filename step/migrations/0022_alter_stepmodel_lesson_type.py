# Generated by Django 4.1.10 on 2023-09-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step', '0021_alter_stepmodel_lesson_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepmodel',
            name='lesson_type',
            field=models.CharField(choices=[('test', 'Тест'), ('video', 'Видео'), ('text', 'Текст')], max_length=10, verbose_name='Тип занятия'),
        ),
    ]
