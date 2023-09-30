from django.contrib.auth import get_user_model
from django.db import models

from modules.models import AbstractModel


class SubscriptionModel(AbstractModel):
    course = models.ForeignKey('modules.CourseModel', on_delete=models.PROTECT, related_name='subscription',
                               verbose_name='Курс')
    price = models.IntegerField(null=False, blank=False, verbose_name='Цена за курс')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    user_subscription = models.ManyToManyField(get_user_model(), through="UsersSubscription")


    def get_total_price(self):
        return self.price

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.course}'
