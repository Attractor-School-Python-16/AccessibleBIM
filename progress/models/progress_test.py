from django.contrib.auth import get_user_model
from django.db import models
from modules.models import AbstractModel


class ProgressTest(AbstractModel):
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Начало тестирования',)
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Конец тестирования')
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="progress",
                             verbose_name="Пользователь")
    test = models.ForeignKey('test_bim.TestBim',
                             related_name='progress',
                             on_delete=models.CASCADE,
                             verbose_name='Тест')
    is_passed = models.BooleanField(verbose_name='Тест пройден', default=False)

    class Meta:
        db_table = 'progress'
        verbose_name = 'Прогрес'
        verbose_name_plural = 'Прогресы'
