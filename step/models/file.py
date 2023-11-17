import os

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


def file_upload_to(instance, filename):
    return os.path.join('steps', 'files', filename)


class FileModel(AbstractModel):
    file_title = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('File title'))
    lesson_file = models.FileField(upload_to=file_upload_to, blank=True, null=True, verbose_name=_('Lesson file'))

    def __str__(self):
        return f'Файл {self.id} {self.file_title}'

    class Meta:
        db_table = 'files'
        verbose_name = _('File')
        verbose_name_plural = _('Files')
