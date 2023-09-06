from django.db import models

from modules.models.modules import AbstractModel


# Create your models here.
class CourseTargetModel(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Для кого предназначен курс')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Подробное описание')

    class Meta:
        db_table = 'Course'
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.title}'
