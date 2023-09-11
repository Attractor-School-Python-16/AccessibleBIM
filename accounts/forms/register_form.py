from django import forms
from captcha.fields import CaptchaField

from accounts.models import CustomUser


class RegisterForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'father_name', 'email', 'password',
                  'phone_number', 'job_title', 'type_corp', 'company']  # нужно добавить 'country'
