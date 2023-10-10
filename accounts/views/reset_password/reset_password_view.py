from django.contrib.auth.views import PasswordResetView
from django.urls import reverse


class ResetPasswordView(PasswordResetView):
    template_name = 'accounts/password-reset/password_reset.html'
    subject_template_name = 'accounts/password-reset/password_reset_subject.txt'
    email_template_name = 'accounts/password-reset/password_reset_email.html'

    def get_success_url(self):
        return reverse('accounts:password_reset_done')
