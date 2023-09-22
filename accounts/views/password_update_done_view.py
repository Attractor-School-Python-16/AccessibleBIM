from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeDoneView


class PasswordUpdateDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "accounts/change_password_done.html"
