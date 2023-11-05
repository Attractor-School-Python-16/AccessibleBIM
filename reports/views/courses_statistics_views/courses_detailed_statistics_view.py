import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.views.generic import DetailView

from modules.models import CourseModel
from modules.models.user_course_progress import UserCourseProgress, CourseProgressStatusChoices
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription


class CoursesDetailedStatisticsView(PermissionRequiredMixin, DetailView):
    template_name = 'statistics/courses_statistics/courses_statistics_detailed.html'
    permission_required = 'accounts.can_view_course_statistics'
    model = CourseModel
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['subscriptions_qty'] = self.get_subscriptions_qty()
        context['completions_qty'] = self.get_completions_qty()
        context['avg_completion_time'] = self.get_avg_completion_time()

        return context

    def get_subscriptions_qty(self, *args, **kwargs):
        course_id = self.object.pk
        return UsersSubscription.objects.filter(subscription__course__pk=course_id
                    ).aggregate(Count('pk')).get('pk__count')

    def get_completions_qty(self, *args, **kwargs):
        course_id = self.object.pk
        steps = StepModel.objects.filter(chapter__course__pk=course_id).order_by('chapter__serial_number', 'serial_number')
        last_step = steps.last()
        return UserCourseProgress.objects.filter(step=last_step, updated_at__isnull=False).count()

    def get_avg_completion_time(self, *args, **kwargs):
        course_id = self.object.pk

        steps = StepModel.objects.filter(chapter__course__pk=course_id).order_by('chapter__serial_number', 'serial_number')
        first_step = steps.first()
        last_step = steps.last()

        end_times = UserCourseProgress.objects.filter(step=last_step, updated_at__isnull=False,
                                                      status=CourseProgressStatusChoices.FINISHED).values('updated_at')
        start_times = UserCourseProgress.objects.filter(step=first_step, status=CourseProgressStatusChoices.FINISHED
                                                        ).values('created_at')

        end_times_list = [elem.get('updated_at') for elem in end_times]
        start_times_list = [elem.get('created_at') for elem in start_times]

        timedelta_list = []
        for pair in zip(end_times_list, start_times_list):
            timedelta_list.append((pair[0] - pair[1]).total_seconds())
        avg_completion_time = sum(timedelta_list) / len(timedelta_list) if timedelta_list else 0
        return datetime.timedelta(seconds=avg_completion_time)
