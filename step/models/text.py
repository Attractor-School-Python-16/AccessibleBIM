from django.db import models
from django.urls import reverse

from modules.models import AbstractModel


class TextModel(AbstractModel):
    text_title = models.CharField(max_length=250, blank=False, null=False, verbose_name="Наименование")
    text_description = models.CharField(max_length=1500, verbose_name="Описание")
    content = models.TextField(max_length=100000, blank=False, null=False, verbose_name="Содержимое")

    def get_absolute_url(self):
        return reverse("step:text_list")
    def __str__(self):
        return f'Текст {self.id} {self.text_title}'

    class Meta:
        db_table = 'texts'
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'