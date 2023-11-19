from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


class StepModel(AbstractModel):
    class TypeChoices(models.TextChoices):
        VIDEO = 'video', _('Video')
        TEXT = 'text', _('Text')
        TEST = 'test', _('Test')

    chapter = models.ForeignKey('modules.ChapterModel', related_name='step', on_delete=models.CASCADE,
                                verbose_name=_('Chapter'), blank=True, null=True)
    title = models.CharField(max_length=250, blank=False, null=False, verbose_name=_('Title'))
    lesson_type = models.CharField(max_length=10, choices=TypeChoices.choices, blank=False, null=False,
                                   verbose_name=_('Lesson type'))
    text = models.ForeignKey('step.TextModel', related_name='step', on_delete=models.RESTRICT, verbose_name=_('Text'),
                             blank=True, null=True)
    video = models.ForeignKey('step.VideoModel', related_name='step', on_delete=models.RESTRICT,
                              verbose_name=_('Video'), blank=True, null=True)
    test = models.ForeignKey('quiz_bim.QuizBim', related_name='step', on_delete=models.RESTRICT, verbose_name=_('Test'),
                             blank=True, null=True)
    file = models.ManyToManyField('step.FileModel', related_name='step', verbose_name=_('Files'), blank=True, null=True)
    learn_time = models.PositiveIntegerField(blank=False, null=False, verbose_name=_('Lesson learn time'))
    serial_number = models.PositiveIntegerField(default=1, verbose_name=_('Serial number'))

    def get_absolute_url(self):
        return reverse("step:step_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'Занятие {self.id} {self.title}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = StepModel.objects.filter(chapter=self.chapter).aggregate(largest=models.Max('serial_number'))[
                'largest']
            if last_id is not None:
                self.serial_number = last_id + 1
        super(StepModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'steps'
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
