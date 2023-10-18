from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from subscription.models.user_subscription import UsersSubscription


class SalesMainStatisticsView(PermissionRequiredMixin, TemplateView):
    template_name = 'statistics/sales_statistics/sales_statistics_main.html'
    permission_required = 'accounts.can_view_sales_statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions_ttl_qty'] = UsersSubscription.objects.count()
        context['active_subscriptions_qty'] = UsersSubscription.objects.filter(is_active=True).count()
        return context
