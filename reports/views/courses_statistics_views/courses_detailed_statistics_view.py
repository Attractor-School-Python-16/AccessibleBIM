from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView


class CoursesDetailedStatisticsView(PermissionRequiredMixin, TemplateView):
    template_name = 'statistics/courses_statistics/courses_statistics_detailed.html'
    permission_required = 'accounts.can_view_course_statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
