from django.contrib.auth.views import PasswordResetDoneView


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'front/accounts/password-reset/password_reset_done.html'
