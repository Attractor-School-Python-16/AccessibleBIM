from django.db import models
from modules.models import AbstractModel


class AnswerBim(AbstractModel):
    answer = models.CharField(max_length=100, verbose_name='Ответ')
    is_correct = models.BooleanField(verbose_name='Валидация ответа',
                                     choices=[(False, 'Неверный ответ'), (True, 'Верный ответ')],
                                     default=False)
    question_bim = models.ForeignKey('quiz_bim.QuestionBim',
                                     related_name='answer_bim',
                                     on_delete=models.CASCADE,
                                     verbose_name='Вопрос')

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        db_table = 'answer_bim'
        verbose_name = 'Ответ Bim'
        verbose_name_plural = 'Ответ Bim'
