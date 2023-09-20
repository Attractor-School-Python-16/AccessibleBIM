from django.contrib.auth.views import PasswordResetView


class ResetPasswordView(PasswordResetView):
    template_name = 'accounts/password-reset/password_reset.html',
    subject_template_name = 'accounts/password-reset/password_reset_subject.txt',
    email_template_name = 'accounts/password-reset/password_reset_email.html',
    success_url = '/password-reset/done/'
