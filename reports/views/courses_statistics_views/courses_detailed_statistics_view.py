from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.views.generic import DetailView

from modules.models import CourseModel
from modules.models.user_course_progress import UserCourseProgress
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription


class CoursesDetailedStatisticsView(PermissionRequiredMixin, DetailView):
    template_name = 'statistics/courses_statistics/courses_statistics_detailed.html'
    permission_required = 'accounts.can_view_course_statistics'
    model = CourseModel
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions_qty'] = UsersSubscription.objects.filter(subscription__course__pk=kwargs.get('pk')
                                                                        ).aggregate(Count('pk')).get('pk__count')

        steps = StepModel.objects.filter(chapter__course__pk=kwargs.get('pk')).order_by('serial_number')
        # first_step = steps.first()
        last_step = steps.last()
        completions_qty = UserCourseProgress.objects.filter(step=last_step).count()
        context['completions_qty'] = completions_qty


        # нужно доработать!!!
        avg_completion_time = 0
        context['avg_completion_time'] = avg_completion_time
        return context
