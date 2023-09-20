from django.shortcuts import render

from django.views import View
from django.views.generic import DetailView

from accounts.models import CustomUser


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_moderator = self.request.user.groups.filter(name='moderators').exists()
        context['is_moderator'] = is_moderator
        return context