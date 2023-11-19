from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView

from modules.models import CourseModel
from subscription.models.user_subscription import UsersSubscription


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'front/accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_subscription'] = UsersSubscription.objects.all().filter(user=self.request.user, is_active=True)
        context['courses'] = CourseModel.objects.filter(Q(subscription__is_published=True) & (
                Q(subscription__users=self.request.user) & Q(subscription__us_subscriptions__is_active=True)))
        return context

