from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.models import AbstractModel


class QuestionBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name=_('Question'))
    test_bim = models.ForeignKey('quiz_bim.QuizBim', related_name='question_bim', on_delete=models.CASCADE,
                                 verbose_name=_('Test'), null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'question_bim'
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
