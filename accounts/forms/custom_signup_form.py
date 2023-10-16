from django import forms
from django.contrib.auth import get_user_model


class CustomSignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'father_name', 'country', 'phone_number', 'job_title', 'type_corp',
                  'company']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.father_name = self.cleaned_data['father_name']
        user.country = self.cleaned_data['country']
        user.phone_number = self.cleaned_data['phone_number']
        user.job_title = self.cleaned_data['job_title']
        user.type_corp = self.cleaned_data['type_corp']
        user.company = self.cleaned_data['company']
        user.email_verified = True
        user.save()
