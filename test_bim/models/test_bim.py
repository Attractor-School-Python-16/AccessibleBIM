from django.db import models
from modules.models.modules import AbstractModel


# Create your models here.


class TestBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Название теста')
    questions_qty = models.IntegerField(verbose_name='Количество вопросов')

    # progress_id = models.ForeignKey('progress.Progress', related_name='test_bim', on_delete=models.CASCADE,
    #                            verbose_name='Прогресс теста')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'test_bim'
        verbose_name = 'Тест Bim'
        verbose_name_plural = 'Тесты Bim'
