from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CourseProgressStatusChoices(models.TextChoices):
    IN_PROGRESS = 0, _("In progress")
    FINISHED = 1, _("Finished")


class UserCourseProgress(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="user_course_progress",
                             verbose_name="Пользователь")
    step = models.ForeignKey('step.StepModel', related_name='step_course_progress', on_delete=models.CASCADE)
    status = models.IntegerField(_("Status"), blank=False, null=False, choices=CourseProgressStatusChoices.choices,
                                 default=0)
    created_at = models.DateTimeField(_("Step start"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Step finish"), auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'user_course_progress'
        verbose_name = _("Course progress")
        verbose_name_plural = _("Course progress")
