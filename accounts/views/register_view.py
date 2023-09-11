from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import RegisterForm
from accounts.models import CustomUser


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    model = CustomUser
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
