from django.db import models
from modules.models import AbstractModel


class TestBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Название теста')
    questions_qty = models.IntegerField(verbose_name='Количество вопросов')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'test_bim'
        verbose_name = 'Тест Bim'
        verbose_name_plural = 'Тесты Bim'
