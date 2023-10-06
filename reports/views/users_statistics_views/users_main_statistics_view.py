from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from subscription.models.user_subscription import UsersSubscription


class UsersMainStatisticsView(TemplateView):
    template_name = 'statistics/users_statistics/users_statistics_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered_users_qty'] = get_user_model().objects.count()
        context['active_subscribers_qty'] = UsersSubscription.objects.filter(is_active=True).count()
        # Должно быть UsersSubscription.objects.filter(is_active=True).distinct('user').count()
        # Но работает только с postgres, не с sqlite
        return context
