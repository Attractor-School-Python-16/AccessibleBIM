from django.contrib.auth import get_user_model
from django.db import models
from modules.models.modules import AbstractModel


# Create your models here.


class ProgressTestAnswers(AbstractModel):
    # user = models.ForeignKey(get_user_model(),
    #                          on_delete=models.CASCADE,
    #                          related_name="user_answers",
    #                          verbose_name="Пользователь")
    progress_test = models.ForeignKey('progress.ProgressTest',
                                      related_name='user_answers',
                                      on_delete=models.CASCADE,
                                      verbose_name='Прогрес теста'
                                      )
    question = models.ForeignKey('test_bim.QuestionBim',
                                 related_name='user_answers',
                                 on_delete=models.CASCADE,
                                 verbose_name='Вопрос')
    answer = models.ForeignKey('test_bim.AnswerBim',
                               related_name='user_answer',
                               on_delete=models.CASCADE,
                               verbose_name='Ответ')

    class Meta:
        db_table = 'progress_answers'
        verbose_name = 'Впопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'
