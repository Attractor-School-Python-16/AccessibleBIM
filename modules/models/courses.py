from django.db import models

from modules.models.modules import AbstractModel, Module


# Create your models here.
class Course(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название модуля')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Описание модуля')
    image = models.ImageField(null=False, blank=False, upload_to='course', verbose_name='Фото для курса')
    module_id = models.ForeignKey(Module, related_name='courses', on_delete=models.CASCADE)
    courseTarget_id = models.ForeignKey(Module, related_name='courses', on_delete=models.DO_NOTHING)
    learnTime = models.IntegerField(null=False, blank=False, default=0, verbose_name='Время на прохождение курса')
    # teacher = models.ManyToManyField('module.Teacher', related_name='teachers', verbose_name='Учителя курса')

    class Meta:
        db_table = 'Course'
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.title}'
