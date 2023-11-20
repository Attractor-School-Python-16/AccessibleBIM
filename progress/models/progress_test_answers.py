from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


class ProgressTestAnswers(AbstractModel):
    progress_test = models.ForeignKey('progress.ProgressTest',
                                      related_name='user_progress',
                                      on_delete=models.CASCADE,
                                      verbose_name=_('Test progress')
                                      )
    question = models.ForeignKey('quiz_bim.QuestionBim',
                                 related_name='user_question',
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Question'))
    answer = models.ForeignKey('quiz_bim.AnswerBim',
                               related_name='user_answer',
                               on_delete=models.CASCADE,
                               verbose_name=_('Answer'))

    class Meta:
        db_table = 'progress_answers'
        verbose_name = _('Question-Answer')
        verbose_name_plural = _('Questions-Answers')
