from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


class CourseTargetModel(AbstractModel):
    title = models.CharField(_('Target title'), max_length=50, null=False, blank=False)
    description = models.TextField(_('Target description'), max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'course_target'
        verbose_name = _('Course target')
        verbose_name_plural = _('Course targets')

    def __str__(self):
        return f'{self.title}'
