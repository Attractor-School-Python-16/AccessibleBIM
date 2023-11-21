from django import forms

from modules.models import TeacherModel


class TeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherModel
        fields = ['first_name', 'last_name', 'father_name', 'job_title', 'corp', 'experience', 'description']
