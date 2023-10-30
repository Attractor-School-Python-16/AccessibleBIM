from django.db import models

from modules.models.module import AbstractModel


class TeacherModel(AbstractModel):
    first_name = models.CharField(max_length=40, null=False, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=40, null=False, blank=False, verbose_name="Фамилия")
    father_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    job_title = models.CharField(max_length=150, null=True, blank=True, verbose_name="Должность")
    corp = models.CharField(max_length=150, null=True, blank=True, verbose_name="Место работы")
    experience = models.CharField(max_length=150, null=True, blank=True, verbose_name="Опыт работы")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="О себе")

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Учителя'
        verbose_name_plural = 'Учитель'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.father_name:
            full_name = "%s %s %s" % (self.first_name, self.last_name, self.father_name)
            return full_name.strip()
        else:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()

