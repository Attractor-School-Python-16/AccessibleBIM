import os
from django.db import models
from modules.models import AbstractModel


def file_upload_to(instance, filename):
    step_pk = instance.id
    if not step_pk:
        step_pk = "unknown"
    return os.path.join(f'step_{str(step_pk)}', 'file', filename)
#принт показывает, что айдишник находится, но сохранять нормаьно не получается


class FileModel(AbstractModel):
    file_title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование")
    lesson_file = models.FileField(upload_to=file_upload_to, blank=False, null=False, verbose_name="Файл занятия")

    def __str__(self):
        return f'Файл {self.id} {self.file_title}'

    class Meta:
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
