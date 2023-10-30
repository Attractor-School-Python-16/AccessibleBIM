from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'front/accounts/password-reset/password_reset_confirm.html'

    def get_success_url(self):
        return reverse('accounts:password_reset_complete')
