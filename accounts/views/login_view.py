from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from accounts.forms.login_form import LoginForm
from accessibleBIM.settings import LOGIN_REDIRECT_URL


class CustomLoginView(LoginView):
    template_name = 'front/accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(LOGIN_REDIRECT_URL)
