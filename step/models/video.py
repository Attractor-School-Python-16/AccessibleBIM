import os
from django.db import models
from modules.models.modules import AbstractModel


def video_upload_to(instance, filename):
    step_pk = instance.step.pk
    if not step_pk:
        step_pk = "unknown"
    return os.path.join('media', str(step_pk), 'video', filename)


class VideoModel(AbstractModel):
    title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование видео")
    description = models.CharField(max_length=500, verbose_name="Описание видео")
    video_file = models.FileField(upload_to=video_upload_to, blank=False, null=False, verbose_name="Файл видео")