from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models.module import AbstractModel


class ChapterModel(AbstractModel):
    course = models.ForeignKey('modules.CourseModel', on_delete=models.CASCADE, related_name='ct_course')
    title = models.CharField(_('Chapter title'), max_length=50, null=False, blank=False)
    description = models.TextField(_('Chapter description'), max_length=150, null=False, blank=False)
    serial_number = models.IntegerField(_('Serial number'), default=1)

    class Meta:
        db_table = 'chapter'
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')



    def save(self, *args, **kwargs):
        # Это означает, что модель еще не сохранена в базе данных
        if self._state.adding:
            # Получаем максимальное значение serial_number из базы данных
            last_id = ChapterModel.objects.filter(course=self.course).aggregate(largest=models.Max('serial_number'))[
                'largest']

            # Агрегация может вернуть None! Сначала проверьте это.
            # Если это не none, просто используйте последний указанный идентификатор (который должен быть наибольшим)
            # и добавьте к нему еще один
            if last_id is not None:
                self.serial_number = last_id + 1

        super(ChapterModel, self).save(*args, **kwargs)

    def __str__(self):
        # FIXME: Из-за того что используется название с полным описанием, возвращаемая строка слишком длинная
        # Те-же хлебные крошки получаются слишком большими, так как они используют __str__
        return f'{self.title} {self.description}'
