# Generated by Django 4.1.10 on 2023-09-19 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0002_alter_progresstestanswers_options_and_more'),
        ('step', '0015_alter_stepmodel_lesson_type'),
        ('quiz_bim', '0004_rename_app'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestBim',
            new_name='QuizBim',
        ),
        migrations.RenameField(
            model_name='quizbim',
            old_name='test_title',
            new_name='title',
        ),
        migrations.AlterModelTable(
            name='quizbim',
            table='quiz_bim',
        ),
        migrations.RunSQL(
            "ALTER TABLE test_bim RENAME TO quiz_bim",
            "ALTER TABLE quiz_bim TO test_bim"
        )
    ]
