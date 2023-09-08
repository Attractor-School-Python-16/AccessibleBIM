from django.db import models
from modules.models import AbstractModel


class StepModel(AbstractModel):
    TYPE_CHOICES = {
        ('video', 'Видео'),
        ('text', 'Текст'),
        ('test', 'Тест')
    }

    chapter = models.ForeignKey('modules.ChapterModel', related_name='step', on_delete=models.CASCADE, verbose_name='Chapter')
    title = models.CharField(max_length=250, blank=False, null=False, verbose_name='Наименование')
    lesson_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False,
                                   verbose_name='Тип занятия')
    text = models.ForeignKey('step.TextModel', related_name='step', on_delete=models.RESTRICT, verbose_name='Текст')
    video = models.ForeignKey('step.VideoModel', related_name='step', on_delete=models.RESTRICT, verbose_name='Видео')
    test = models.ForeignKey('test_bim.TestBim', related_name='step', on_delete=models.RESTRICT, verbose_name='Тест')
    file = models.ManyToManyField('step.FileModel', related_name='step', verbose_name='Файл')
    learn_time = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f'Занятие {self.id} {self.title}'

    class Meta:
        db_table = 'steps'
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
