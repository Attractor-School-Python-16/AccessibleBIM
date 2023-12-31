# Generated by Django 4.1.10 on 2023-09-20 19:25

from django.db import migrations, models
import django.db.models.deletion
import modules.models.courses
import modules.models.module


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=50, verbose_name='Название курса')),
                ('description', models.TextField(max_length=150, verbose_name='Описание курса')),
                ('image', models.ImageField(upload_to=modules.models.courses.courses_upload_to, verbose_name='Фото для курса')),
                ('language', models.CharField(choices=[('RU', 'Русский'), ('KG', 'Кыргызский'), ('EN', 'Английский')], max_length=10, verbose_name='Язык занятия')),
                ('learnTime', models.IntegerField(default=0, verbose_name='Время на прохождение курса')),
            ],
            options={
                'verbose_name': 'Модуль',
                'verbose_name_plural': 'Модули',
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='CourseTargetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=50, verbose_name='Для кого предназначен курс')),
                ('description', models.TextField(blank=True, max_length=150, null=True, verbose_name='Подробное описание')),
            ],
            options={
                'verbose_name': 'Целевая аудитория',
                'verbose_name_plural': 'Целевая аудитория',
                'db_table': 'course_target',
            },
        ),
        migrations.CreateModel(
            name='ModuleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=50, verbose_name='Название модуля')),
                ('description', models.TextField(max_length=150, verbose_name='Описание модуля')),
                ('image', models.ImageField(upload_to=modules.models.module.module_upload_to, verbose_name='Фото для модуля')),
            ],
            options={
                'verbose_name': 'Модуль',
                'verbose_name_plural': 'Модули',
                'db_table': 'module',
            },
        ),
        migrations.CreateModel(
            name='TeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('first_name', models.CharField(max_length=40, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=40, verbose_name='Фамилия')),
                ('father_name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отчество')),
                ('job_title', models.CharField(blank=True, max_length=150, null=True, verbose_name='Должность')),
                ('corp', models.CharField(blank=True, max_length=150, null=True, verbose_name='Место работы')),
                ('experience', models.CharField(blank=True, max_length=150, null=True, verbose_name='Опыт работы')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='О себе')),
            ],
            options={
                'verbose_name': 'Учителя',
                'verbose_name_plural': 'Учитель',
                'db_table': 'teacher',
            },
        ),
        migrations.CreateModel(
            name='CourseTeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('ct_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='modules.coursemodel', verbose_name='Курсы')),
                ('ct_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='modules.teachermodel', verbose_name='Учителя')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='courseTarget_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='modules.coursetargetmodel'),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='module_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='modules.modulemodel'),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='teachers',
            field=models.ManyToManyField(related_name='courses', through='modules.CourseTeacherModel', to='modules.teachermodel'),
        ),
        migrations.CreateModel(
            name='ChapterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=50, verbose_name='Название главы')),
                ('description', models.TextField(max_length=150, verbose_name='Описание главы')),
                ('serial_number', models.IntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ct_course', to='modules.coursemodel', verbose_name='Курсы')),
            ],
            options={
                'verbose_name': 'Главы',
                'verbose_name_plural': 'Глава',
                'db_table': 'chapter',
            },
        ),
    ]
