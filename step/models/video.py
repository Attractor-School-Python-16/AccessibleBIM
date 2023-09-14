import os
from django.db import models
from modules.models import AbstractModel



def video_upload_to(instance, filename):
    step_pk = instance.id
    if not step_pk:
        step_pk = "unknown"
    return os.path.join(f'step_{str(step_pk)}', 'video', filename)
#принт показывает, что айдишник находится, но сохранять нормаьно не получается


class VideoModel(AbstractModel):
    video_title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование видео")
    video_description = models.CharField(max_length=500, verbose_name="Описание видео")
    video_file = models.FileField(upload_to=video_upload_to, blank=False, null=False, verbose_name="Файл видео")

    def __str__(self):
        return f'Видео {self.id} {self.video_title}'

    class Meta:
        db_table = 'videos'
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
