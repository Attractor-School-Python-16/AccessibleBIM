# Generated by Django 4.1.10 on 2023-09-12 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionmodel',
            name='end_date',
        ),
    ]
