# Generated by Django 4.1.10 on 2023-09-29 16:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_merge_20230924_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='country'),
        ),
    ]