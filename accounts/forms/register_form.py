from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class RegisterForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'father_name', 'email', 'password1',
                  'password2', 'phone_number', 'job_title', 'type_corp', 'company']  # нужно добавить 'country'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })