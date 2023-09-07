from django.db import models

from modules.models.modules import AbstractModel


# Create your models here.
class ChapterModel(AbstractModel):
    course = models.ForeignKey('modules.CourseModel', on_delete=models.CASCADE, related_name='ct_course',
                               verbose_name='Курсы')
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название модуля')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Описание модуля')
    serial_number = models.IntegerField(default=1)

    class Meta:
        db_table = 'Chapter'
        verbose_name = 'Главы'
        verbose_name_plural = 'Глава'

    def save(self, *args, **kwargs):
        # Это означает, что модель еще не сохранена в базе данных
        if self._state.adding:
            # Получаем максимальное значение serial_number из базы данных
            last_id = ChapterModel.objects.filter(customer=self.course).aggregate(largest=models.Max('serial_number'))[
                'largest']

            # Агрегация может вернуть None! Сначала проверьте это.
            # Если это не none, просто используйте последний указанный идентификатор (который должен быть наибольшим)
            # и добавьте к нему еще один
            if last_id is not None:
                self.serial_number = last_id + 1

        super(ChapterModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.description}'
