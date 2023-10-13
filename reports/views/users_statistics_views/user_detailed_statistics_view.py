from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView


class UserDetailedStatisticsView(PermissionRequiredMixin, DetailView):
    template_name = 'statistics/users_statistics/user_detailed_statistics.html'
    permission_required = 'accounts.can_view_user_statistics'
    model = get_user_model()
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_course'] = self.object.get_current_course()
        context['past_courses'] = self.object.get_past_courses()
        return context
