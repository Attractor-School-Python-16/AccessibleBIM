# Generated by Django 4.1.10 on 2023-09-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0009_alter_coursemodel_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='language',
            field=models.CharField(choices=[('RU', 'Русский'), ('KG', 'Кыргызский'), ('EN', 'Английский')], max_length=10, verbose_name='Язык занятия'),
        ),
    ]
