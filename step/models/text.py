from django.db import models


# from courses.models.modules import AbstractModel


class TextModel(AbstractModel):
    title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование")
    description = models.CharField(max_length=500, verbose_name="Описание")
    content = models.TextField(max_length=100000, blank=False, null=False, verbose_name="Содержимое")
