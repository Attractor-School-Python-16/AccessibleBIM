from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models

from modules.models import AbstractModel
from subscription.models import SubscriptionModel


def get_deadline():
    return datetime.now() + timedelta(days=30)

class UsersSubscription(AbstractModel):
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE, related_name='us_subscriptions',
                                     verbose_name='Подписки')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='us_users',
                             verbose_name='Пользователи')
    end_time = models.DateTimeField(default=get_deadline(), verbose_name='Дата окончания подписки')
    is_active = models.BooleanField(default=True, null=False, blank=False, verbose_name="Активность подписки")
