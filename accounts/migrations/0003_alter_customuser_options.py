# Generated by Django 4.1.10 on 2023-09-22 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('can_view_admin_panel', 'Can view admin panel'),)},
        ),
    ]
