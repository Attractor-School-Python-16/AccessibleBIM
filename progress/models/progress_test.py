from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.db import models
from modules.models import AbstractModel


# TODO: Стоит также переименовать ProgressTest в ProgressQuiz
# И тоже самое с полями
class ProgressTest(AbstractModel):
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Начало тестирования',)
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Конец тестирования')
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="progress",
                             verbose_name="Пользователь")
    test = models.ForeignKey('quiz_bim.QuizBim',
                             related_name='progress',
                             on_delete=models.CASCADE,
                             verbose_name='Тест')
    is_passed = models.BooleanField(verbose_name='Тест пройден', default=False)
    in_progress = models.BooleanField(verbose_name='Тест в процессе', default=True)

    def __str__(self):
        return f'User {self.user.pk} Test{self.test.pk}'

    def correct_answers(self):
        return self.user_progress.filter(answer__is_correct=True).count()

    def accuracy(self):
        return self.correct_answers() / self.user_progress.count()

    def is_overdue(self):
        return (datetime.now(timezone.utc) - self.start_time) > timedelta(hours=2)

    class Meta:
        db_table = 'progress'
        verbose_name = 'Прогрес'
        verbose_name_plural = 'Прогресы'
