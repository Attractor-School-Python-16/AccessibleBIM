# Generated by Django 4.1.10 on 2023-10-13 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_alter_subscriptionmodel_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionmodel',
            name='user_subscription',
        ),
    ]