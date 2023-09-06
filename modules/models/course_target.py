from django.db import models

from modules.models.courses import CourseModel
from modules.models.modules import AbstractModel


# Create your models here.
class CourseTargetModel(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Для кого предназначен курс')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Подробное описание')
    courseTarget_id = models.ForeignKey(CourseModel, related_name='courses', on_delete=models.CASCADE)

    class Meta:
        db_table = 'CourseTarget'
        verbose_name = 'Целевая аудитория'
        verbose_name_plural = 'Целевая аудитория'

    def __str__(self):
        return f'{self.title}'
