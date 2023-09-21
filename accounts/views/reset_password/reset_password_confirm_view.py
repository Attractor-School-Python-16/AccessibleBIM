from django.contrib.auth.views import PasswordResetConfirmView


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password-reset/password_reset_confirm.html'
    success_url = '/password-reset-complete/'
