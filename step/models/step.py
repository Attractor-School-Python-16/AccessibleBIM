from django.db import models
# from modules.models.modules import AbstractModel



class StepModel(AbstractModel):
    TYPE_CHOICES = {
        ('video', 'Видео'),
        ('text', 'Текст'),
        ('test', 'Тест')
    }

    # chapter = models.ForeignKey('modules.ChapterModel', related_name='step', on_delete=models.CASCADE, verbose_name='Chapter')
    title = models.CharField(max_length= 250, blank=False, null=False)
    lesson_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)
    # text = models.ForeignKey('step.Text', related_name='step', on_delete=models.RESTRICT, verbose_name='Текст')
    # video = models.ForeignKey('step.Video', related_name='step', on_delete=models.RESTRICT, verbose_name='Видео')
    # test = models.ForeignKey('step.Test', related_name='step', on_delete=models.RESTRICT, verbose_name='Тест')
    # file = models.ManyToManyField('step.File', related_name='step', verbose_name='Файл')
    learn_time = models.PositiveIntegerField(blank=False, null=False)
