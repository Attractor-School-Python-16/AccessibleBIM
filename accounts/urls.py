from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from accounts.views import RegisterView, ProfileView, VerificationEmailSentView, VerificationEmailNotSentView, \
    InvalidVerificationLinkView
from accounts.views.register_view import activate

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verification/', VerificationEmailSentView.as_view(), name="verification_sent"),
    path('email-verification/sending-error/', VerificationEmailNotSentView.as_view(), name="verification_sending_error"),
    path('email-verification/invalid-link/', InvalidVerificationLinkView.as_view(), name="invalid_verification_link"),
    path('email-verification/<uidb64>/<token>', activate, name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(
        template_name="accounts/change_password.html",
        success_url='/password-change/done/'), name="change_password"),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name="accounts/change_password_done.html"),
        name='change_password_done'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password-reset/password_reset.html',
        subject_template_name='accounts/password-reset/password_reset_subject.txt',
        email_template_name='accounts/password-reset/password_reset_email.html',
        success_url='/password-reset/done/'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password-reset/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password-reset/password_reset_confirm.html',
        success_url='/password-reset-complete/'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password-reset/password_reset_complete.html'), name='password_reset_complete'),
]
