from django.contrib.auth import get_user_model
from django.db import models

from modules.models import AbstractModel
from subscription.models import SubscriptionModel


class UsersSubscription(AbstractModel):
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE, related_name='us_subscriptions',
                                     verbose_name='Подписки')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='us_users',
                             verbose_name='Пользователи')
