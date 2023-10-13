import os
from django.db import models
from django.urls import reverse

from modules.models import AbstractModel
from django_ffmpeg.models import Video as FFmpegVideo


def video_upload_to(instance, filename):
    return os.path.join('steps', 'videos', 'orig', filename)
#изменила логику сохранения, добавила еще одну папку orig. Остальное по аналогии с функцией в модели файла


class VideoModel(AbstractModel):
    video_title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование видео")
    video_description = models.CharField(max_length=500, verbose_name="Описание видео")
    video_file = models.FileField(upload_to=video_upload_to, blank=False, null=False, verbose_name="Файл видео")
    converted_video = models.ForeignKey(FFmpegVideo, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, user=None, *args, **kwargs):
        if not self.converted_video:
            ffmpeg_video = FFmpegVideo.objects.create(
                video=self.video_file,
                user=user
            )
            self.converted_video = ffmpeg_video
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("step:video_list")
    def __str__(self):
        return f'Видео {self.id} {self.video_title}'

    class Meta:
        db_table = 'videos'
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'






