# Generated by Django 4.1.10 on 2023-09-14 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0007_alter_coursemodel_image'),
        ('test_bim', '0002_rename_title_testbim_test_title'),
        ('step', '0007_remove_stepmodel_file_alter_stepmodel_lesson_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepmodel',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='step', to='modules.chaptermodel', verbose_name='Chapter'),
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='lesson_type',
            field=models.CharField(choices=[('test', 'Тест'), ('video', 'Видео'), ('text', 'Текст')], max_length=10, verbose_name='Тип занятия'),
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='step', to='test_bim.testbim', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='step', to='step.textmodel', verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='step', to='step.videomodel', verbose_name='Видео'),
        ),
    ]
