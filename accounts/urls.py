from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import path

from accounts.views import RegisterView, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(template_name="accounts/change_password.html",
                                                        success_url='/password-change/done/'), name="change_password"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="accounts/change_password_done.html"),
         name='change_password_done'),
]
