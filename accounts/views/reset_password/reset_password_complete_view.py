from django.contrib.auth.views import PasswordResetCompleteView


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password-reset/password_reset_complete.html'
