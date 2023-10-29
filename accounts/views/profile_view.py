from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from modules.models import CourseModel
from subscription.models.user_subscription import UsersSubscription


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'front/accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription = UsersSubscription.objects.all().filter(user=self.request.user)
        for subs in user_subscription:
            context['courses'] = CourseModel.objects.all().filter(course=subs.subscription.id)
        return context

