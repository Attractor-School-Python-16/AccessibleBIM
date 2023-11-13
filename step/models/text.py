from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


class TextModel(AbstractModel):
    text_title = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Text title'))
    text_description = models.CharField(max_length=1500, blank=True, null=True, verbose_name=_('Text description'))
    content = models.TextField(max_length=100000, blank=True, null=True, verbose_name=_('Text content'))

    def get_absolute_url(self):
        return reverse("step:text_list")

    def __str__(self):
        return f'Текст {self.id} {self.text_title}'

    class Meta:
        db_table = 'texts'
        verbose_name = _('Text')
        verbose_name_plural = _('Texts')
