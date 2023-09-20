from django.db import models

from modules.models import AbstractModel


class ProgressTestAnswers(AbstractModel):
    progress_test = models.ForeignKey('progress.ProgressTest',
                                      related_name='user_progress',
                                      on_delete=models.CASCADE,
                                      verbose_name='Прогресс теста'
                                      )
    question = models.ForeignKey('quiz_bim.QuestionBim',
                                 related_name='user_question',
                                 on_delete=models.CASCADE,
                                 verbose_name='Вопрос')
    answer = models.ForeignKey('quiz_bim.AnswerBim',
                               related_name='user_answer',
                               on_delete=models.CASCADE,
                               verbose_name='Ответ')

    class Meta:
        db_table = 'progress_answers'
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'
