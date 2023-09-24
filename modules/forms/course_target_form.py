from django import forms

from modules.models import CourseTargetModel


class CourseTargetForm(forms.ModelForm):
    class Meta:
        model = CourseTargetModel
        fields = ['title', 'description']
