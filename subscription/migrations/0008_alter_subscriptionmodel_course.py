# Generated by Django 4.1.10 on 2023-09-30 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0006_alter_chaptermodel_options_alter_coursemodel_options'),
        ('subscription', '0007_subscriptionmodel_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionmodel',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscription', to='modules.coursemodel', verbose_name='Курс'),
        ),
    ]
