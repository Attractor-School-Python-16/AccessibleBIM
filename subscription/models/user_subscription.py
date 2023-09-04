from django.contrib.auth import get_user_model
from django.db import models

from subscription.models.subscription import AbstractModel, Subscription


# Create your models here.
class UsersSubscription(AbstractModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, related_name='us_subscriptions',
                                     verbose_name='Подписки')
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='us_users',
                             verbose_name='Пользователи')
