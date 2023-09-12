from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
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
    path('password-change/', PasswordChangeView.as_view(template_name="accounts/change_password.html",
                                                        success_url='/password-change/done/'), name="change_password"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="accounts/change_password_done.html"),
         name='change_password_done'),
]
