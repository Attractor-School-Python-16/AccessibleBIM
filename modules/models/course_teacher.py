from django.db import models

from modules.models.courses import CourseModel
from modules.models.modules import AbstractModel
from modules.models.teacher import TeacherModel


# Create your models here.
class CourseTeacherModel(AbstractModel):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name='ct_course',
                               verbose_name='Курсы')
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='ct_teacher',
                                verbose_name='Учителя')

