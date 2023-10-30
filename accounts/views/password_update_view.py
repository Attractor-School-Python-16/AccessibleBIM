from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    template_name = "front/accounts/change_password.html"
    success_url = '/password-change/done/'
