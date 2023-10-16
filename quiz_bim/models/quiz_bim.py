from django.db import models
from modules.models import AbstractModel


class QuizBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Тема тестирования', blank=True, null=True)
    questions_qty = models.PositiveIntegerField(verbose_name='Количество вопросов для прохождения', blank=True,
                                                null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'quiz_bim'
        verbose_name = 'Тест Bim'
        verbose_name_plural = 'Тесты Bim'
