import os
from django.db import models
from django.urls import reverse

from modules.models import AbstractModel


def file_upload_to(instance, filename):
    return os.path.join('steps', 'files', filename)
#пока оставил так, смысла сохранять по id не вижу, можно вместо filename использовать instance.file_title


class FileModel(AbstractModel):
    file_title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Наименование")
    lesson_file = models.FileField(upload_to=file_upload_to, blank=True, null=True, verbose_name="Файл занятия")

    def get_absolute_url(self):
        return reverse("step:file_list")

    def __str__(self):
        return f'Файл {self.id} {self.file_title}'

    class Meta:
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
