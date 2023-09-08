from django.db import models

from modules.models import AbstractModel


# Create your models here.
class CourseTeacherModel(AbstractModel):
    ct_course = models.ForeignKey('modules.CourseModel', on_delete=models.CASCADE, related_name='course',
                               verbose_name='Курсы')
    ct_teacher = models.ForeignKey('modules.TeacherModel', on_delete=models.CASCADE, related_name='teacher',
                                verbose_name='Учителя')

