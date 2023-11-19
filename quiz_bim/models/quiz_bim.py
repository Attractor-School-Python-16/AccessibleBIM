from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.models import AbstractModel


class QuizBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name=_('Test title'), blank=True, null=True)
    questions_qty = models.PositiveIntegerField(verbose_name=_('Questions quantity'), default=0,
                                                blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'quiz_bim'
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')
