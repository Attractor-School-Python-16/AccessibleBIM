from django.db import models

from modules.models import AbstractModel


class SubscriptionModel(AbstractModel):
    course = models.ForeignKey('modules.CourseModel', on_delete=models.PROTECT, related_name='modules', verbose_name='Курс')
    price = models.IntegerField(null=False, blank=False, verbose_name='Цена за курс')
    discount = models.IntegerField(null=True, blank=True, default=0, verbose_name='Скидка на курс')
    end_date = models.DateTimeField(verbose_name='Дата обновления')

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'{self.course}'
