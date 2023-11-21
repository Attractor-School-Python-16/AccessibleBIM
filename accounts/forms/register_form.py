from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class RegisterForm(UserCreationForm):
    captcha = CaptchaField(label=_('captcha'))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'father_name', 'email', 'password1', 'password2',
                  'country', 'phone_number', 'job_title', 'type_corp', 'company']
