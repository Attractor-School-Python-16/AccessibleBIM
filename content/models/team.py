from django.db import models

from modules.models import AbstractModel


class TeamModel(AbstractModel):
    photo = models.ImageField(verbose_name='Photo', upload_to='team')
    name = models.CharField(verbose_name='Name', max_length=150)
    title = models.CharField(verbose_name='Title', max_length=150)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'
        verbose_name = 'Team'
        verbose_name_plural = 'Team'
