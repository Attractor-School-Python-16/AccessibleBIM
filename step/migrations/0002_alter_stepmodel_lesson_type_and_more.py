from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepmodel',
            name='lesson_type',
            field=models.CharField(choices=[('video', 'Видео'), ('text', 'Текст'), ('test', 'Тест')], max_length=10, verbose_name='Тип занятия'),
        ),
        migrations.AlterField(
            model_name='stepmodel',
            name='serial_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]