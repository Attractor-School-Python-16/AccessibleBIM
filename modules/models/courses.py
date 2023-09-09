from django.db import models

from modules.models.teacher import TeacherModel
from modules.models.module import AbstractModel
from modules.models.course_teacher import CourseTeacherModel


class CourseModel(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название модуля')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Описание модуля')
    image = models.ImageField(null=False, blank=False, upload_to='course', verbose_name='Фото для курса')
    module_id = models.ForeignKey('modules.ModuleModel', related_name='courses', on_delete=models.CASCADE)
    courseTarget_id = models.ForeignKey('modules.CourseTargetModel', related_name='courses', on_delete=models.DO_NOTHING)
    learnTime = models.IntegerField(null=False, blank=False, default=0, verbose_name='Время на прохождение курса')
    teachers = models.ManyToManyField(TeacherModel, related_name='courses', through=CourseTeacherModel,
                                      through_fields=('ct_course', 'ct_teacher'))

    class Meta:
        db_table = 'course'
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.title}'
