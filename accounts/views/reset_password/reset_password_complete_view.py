from django.contrib.auth.views import PasswordResetCompleteView


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'front/accounts/password-reset/password_reset_complete.html'
