import os
from django.db import models
from django.urls import reverse

from modules.models import AbstractModel



def video_upload_to(instance, filename):
    return os.path.join('steps', 'videos', filename)
#по аналогии с функцией в модели файла


class VideoModel(AbstractModel):
    video_title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Наименование видео")
    video_description = models.CharField(max_length=500, blank=True, null=True, verbose_name="Описание видео")
    video_file = models.FileField(upload_to=video_upload_to, blank=True, null=True, verbose_name="Файл видео")


    def get_absolute_url(self):
        return reverse("step:video_list")
    def __str__(self):
        return f'Видео {self.id} {self.video_title}'

    class Meta:
        db_table = 'videos'
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
