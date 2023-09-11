from django import forms

from accounts.models import CustomUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'father_name', 'email', 'password',
                  'phone_number', 'job_title', 'company']  # нужно добавить 'country'
