from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, VerificationEmailSentView, VerificationEmailNotSentView, \
    InvalidVerificationLinkView, PasswordUpdateView, PasswordUpdateDoneView, ResetPasswordView, ResetPasswordDoneView, \
    ResetPasswordConfirmView, ResetPasswordCompleteView, GrantModeratorPanelView
from accounts.views.grant_moderator import GrantModerators, RemoveModerators
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
    path('password-change/', PasswordUpdateView.as_view(), name="change_password"),
    path('password-change/done/', PasswordUpdateDoneView.as_view(), name='change_password_done'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('grant-moderators-panel/', GrantModeratorPanelView.as_view(), name='grant_moderator_panel'),
    path('grant-moderators/', GrantModerators.as_view(), name='grant_moderators'),
    path('remove-moderators/', RemoveModerators.as_view(), name='remove_moderators'),
]
