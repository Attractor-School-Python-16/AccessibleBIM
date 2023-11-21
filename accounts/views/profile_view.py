from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from modules.models import CourseModel
from progress.models import ProgressTest
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'front/accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_subscription'] = UsersSubscription.objects.all().filter(user=self.request.user, is_active=True)
        progress_quiz_query = ProgressTest.objects.filter(user=self.request.user, in_progress=True, is_passed=False)
        overdue_quiz_pk = []
        for progress_quiz in progress_quiz_query:
            if progress_quiz.is_overdue():
                overdue_quiz_pk.append(progress_quiz.pk)
        step_quiz = StepModel.objects.filter(step_course_progress__user=self.request.user,
                                             test__progress__in_progress=True,
                                             test__progress__pk__in=overdue_quiz_pk)
        context['step_quiz_query'] = step_quiz
        context['courses'] = CourseModel.objects.filter(Q(subscription__is_published=True) & (
                Q(subscription__users=self.request.user) & Q(subscription__us_subscriptions__is_active=True)))
        return context

