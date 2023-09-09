from django.db import models

from modules.models import AbstractModel


class CourseTargetModel(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Для кого предназначен курс')
    description = models.TextField(max_length=150, null=True, blank=True, verbose_name='Подробное описание')

    class Meta:
        db_table = 'course_target'
        verbose_name = 'Целевая аудитория'
        verbose_name_plural = 'Целевая аудитория'

    def __str__(self):
        return f'{self.title}'
