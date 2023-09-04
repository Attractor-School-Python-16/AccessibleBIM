from django.contrib.auth import get_user_model
from django.db import models

from subscription.models.subscription import AbstractModel, Subscription


# Create your models here.
class UsersSubscription(AbstractModel):
    subscription = models.ManyToManyField(Subscription, related_name='subscriptions', verbose_name='Подписки')
    user = models.ManyToManyField(get_user_model(), related_name='users', verbose_name='Пользователи')
