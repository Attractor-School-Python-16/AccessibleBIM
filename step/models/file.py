import os
from django.db import models


# from courses.models.modules import AbstractModel

def file_upload_to(instance, filename):
    step_pk = instance.step.pk
    if not step_pk:
        step_pk = "unknown"
    return os.path.join('media', str(step_pk), 'file', filename)


class FileModel(AbstractModel):
    lesson_file = models.FileField(upload_to=file_upload_to, blank=False, null=False, verbose_name="Файл занятия")
