from django.shortcuts import render

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from accounts.models import CustomUser


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


