# Generated by Django 4.1.10 on 2023-11-08 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0009_alter_modulemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chaptermodel',
            options={'verbose_name': 'Chapter', 'verbose_name_plural': 'Chapters'},
        ),
        migrations.AlterField(
            model_name='chaptermodel',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ct_course', to='modules.coursemodel'),
        ),
        migrations.AlterField(
            model_name='chaptermodel',
            name='description',
            field=models.TextField(max_length=150, verbose_name='Chapter description'),
        ),
        migrations.AlterField(
            model_name='chaptermodel',
            name='serial_number',
            field=models.IntegerField(default=1, verbose_name='Serial number'),
        ),
        migrations.AlterField(
            model_name='chaptermodel',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Chapter title'),
        ),
    ]