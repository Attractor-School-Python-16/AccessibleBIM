from django import template

from subscription.models.user_subscription import UsersSubscription
from django.db.models import Q

register = template.Library()


@register.filter(name='user_subs')
def user_subs(user_pk):
    try:
        subs = UsersSubscription.objects.get(Q(user_id=user_pk) & Q(is_active=True))
        return subs.subscription
    except UsersSubscription.DoesNotExist:
        return False
