# Generated by Django 4.1.13 on 2023-11-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_bim', '0002_alter_questionbim_test_bim_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizbim',
            name='questions_qty',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Количество вопросов для прохождения'),
        ),
    ]
