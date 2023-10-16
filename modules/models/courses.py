import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models.teacher import TeacherModel
from modules.models.module import AbstractModel
from modules.models.course_teacher import CourseTeacherModel


def courses_upload_to(instance, filename):
    courses = instance.title
    if not courses:
        courses = "unknown"
    return os.path.join('courses', str(courses), 'image', filename)


class CourseModel(AbstractModel):
    class TypeChoices(models.TextChoices):
        RU = 'RU', _('Русский')
        EN = 'EN', _('Английский')
        KG = 'KG', _('Кыргызский')

    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название курса')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Описание курса')
    image = models.ImageField(null=False, blank=False, upload_to=courses_upload_to, verbose_name='Фото для курса')
    module_id = models.ForeignKey('modules.ModuleModel', related_name='courses', on_delete=models.CASCADE)
    courseTarget_id = models.ForeignKey('modules.CourseTargetModel', related_name='courses',
                                        on_delete=models.DO_NOTHING)
    language = models.CharField(max_length=10, choices=TypeChoices.choices, blank=False, null=False,
                                   verbose_name='Язык занятия')
    learnTime = models.IntegerField(null=False, blank=False, default=0, verbose_name='Время на прохождение курса (часы)')
    teachers = models.ManyToManyField(TeacherModel, related_name='courses', through=CourseTeacherModel,
                                      through_fields=('ct_course', 'ct_teacher'))

    class Meta:
        db_table = 'course'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self.title}'
