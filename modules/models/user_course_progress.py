from django.db import models
from django.contrib.auth import get_user_model


class UserCourseProgress(models.Model):
    STATUSES = ['finished', 'in_progress']

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="user_course_progress",
                             verbose_name="Пользователь")
    step = models.ForeignKey('step.StepModel', on_delete=models.CASCADE)
    status = models.CharField(max_length=55, blank=False, null=False, choices=STATUSES, default='in_progress',
                              verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Начало шага')
    updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Конец шага')

    class Meta:
        db_table = 'user_course_progress'
        verbose_name = 'Прогресс по курсу'
        verbose_name_plural = 'Прогрессы по курсу'