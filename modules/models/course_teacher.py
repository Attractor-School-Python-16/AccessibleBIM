from django.db import models

from modules.models.courses import Course
from modules.models.modules import AbstractModel
from modules.models.teacher import Teacher


# Create your models here.
class CourseTeacher(AbstractModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ct_course',
                               verbose_name='Курсы')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ct_teacher',
                                verbose_name='Учителя')

