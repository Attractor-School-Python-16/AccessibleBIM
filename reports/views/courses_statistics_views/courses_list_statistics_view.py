from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from modules.models import CourseModel


class CoursesListStatisticsView(PermissionRequiredMixin, ListView):
    template_name = "statistics/courses_statistics/courses_list_statistics.html"
    permission_required = 'accounts.can_view_course_statistics'
    model = CourseModel
    context_object_name = 'courses'
