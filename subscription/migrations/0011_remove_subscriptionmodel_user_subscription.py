# Generated by Django 4.1.10 on 2023-11-07 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_subscriptionmodel_user_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionmodel',
            name='user_subscription',
        ),
    ]
