from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView


class UsersListStatisticsView(PermissionRequiredMixin, ListView):
    template_name = "statistics/users_statistics/users_list_statistics.html"
    permission_required = 'accounts.can_view_user_statistics'
    model = get_user_model()
    context_object_name = 'people'
