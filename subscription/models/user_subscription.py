from django.contrib.auth import get_user_model
from django.db import models
from modules.models import AbstractModel
from subscription.models import SubscriptionModel
from django.utils.translation import gettext_lazy as _


class UsersSubscription(AbstractModel):
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE, related_name='us_subscriptions',
                                     verbose_name=_("Subscriptions"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='us_users',
                             verbose_name=_("Users"))
    end_time = models.DateTimeField(verbose_name=_("Subscription expire date"))
    is_active = models.BooleanField(default=True, null=False, blank=False, verbose_name=_("Subscription enabled"))

    def __str__(self):
        return f'{self.pk}, {self.subscription}, {self.user}, {self.end_time}, {self.is_active}'
