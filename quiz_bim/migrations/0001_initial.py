# Generated by Django 4.1.10 on 2023-09-07 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestBim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=100, verbose_name='Название теста')),
                ('questions_qty', models.IntegerField(verbose_name='Количество вопросов')),
            ],
            options={
                'verbose_name': 'Тест Bim',
                'verbose_name_plural': 'Тесты Bim',
                'db_table': 'test_bim',
            },
        ),
        migrations.CreateModel(
            name='QuestionBim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=100, verbose_name='Вопрос')),
                ('test_bim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_bim', to='quiz_bim.testbim', verbose_name='Тест Bim')),
            ],
            options={
                'verbose_name': 'Вопрос Bim',
                'verbose_name_plural': 'Вопрос Bim',
                'db_table': 'question_bim',
            },
        ),
        migrations.CreateModel(
            name='AnswerBim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('answer', models.CharField(max_length=100, verbose_name='Ответ')),
                ('is_correct', models.BooleanField(choices=[(False, 'Неверный ответ'), (True, 'Верный ответ')], default=False, verbose_name='Валидация ответа')),
                ('question_bim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_bim', to='quiz_bim.questionbim', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ Bim',
                'verbose_name_plural': 'Ответ Bim',
                'db_table': 'answer_bim',
            },
        ),
    ]
