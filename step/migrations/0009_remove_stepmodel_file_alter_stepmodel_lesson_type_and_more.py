# Generated by Django 4.1.10 on 2023-09-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step', '0008_alter_stepmodel_chapter_alter_stepmodel_lesson_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stepmodel',
            name='file',
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='lesson_type',
            field=models.CharField(choices=[('text', 'Текст'), ('test', 'Тест'), ('video', 'Видео')], max_length=10, verbose_name='Тип занятия'),
        ),
        migrations.AddField(
            model_name='stepmodel',
            name='file',
            field=models.ManyToManyField(blank=True, null=True, related_name='step', to='step.filemodel', verbose_name='Файлы'),
        ),
    ]
