from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from modules.models import CourseModel
from subscription.models import SubscriptionModel


class CoursesMainStatisticsView(PermissionRequiredMixin, TemplateView):
    template_name = 'statistics/courses_statistics/courses_statistics_main.html'
    permission_required = 'accounts.can_view_course_statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses_ttl_qty'] = CourseModel.objects.count()
        context['published_courses_qty'] = SubscriptionModel.objects.filter(is_published=True).count()
        return context
