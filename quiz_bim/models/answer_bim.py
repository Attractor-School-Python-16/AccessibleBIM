from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.models import AbstractModel


class AnswerBim(AbstractModel):
    answer = models.CharField(max_length=100, verbose_name=_('Answer'))
    is_correct = models.BooleanField(verbose_name=_('Answer validation'),
                                     choices=[(False, _('Wrong answer')), (True, _('Right answer'))],
                                     default=False)
    question_bim = models.ForeignKey('quiz_bim.QuestionBim',
                                     related_name='answer_bim',
                                     on_delete=models.CASCADE,
                                     verbose_name=_('Question'))

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        db_table = 'answer_bim'
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
