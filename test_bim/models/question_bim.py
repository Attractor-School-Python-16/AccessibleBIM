from django.db import models
from modules.models.modules import AbstractModel


# Create your models here.


class QuestionBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Вопрос')
    test_bim = models.ForeignKey('test_bim.TestBim', related_name='question_bim', on_delete=models.CASCADE,
                                 verbose_name='Тест Bim')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'question_bim'
        verbose_name = 'Вопрос Bim'
        verbose_name_plural = 'Вопрос Bim'
