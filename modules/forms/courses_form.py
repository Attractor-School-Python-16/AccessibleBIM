from django import forms

from modules.models import CourseModel


class CoursesForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = ['title', 'description', 'image', 'learnTime', 'courseTarget_id', 'language', 'teachers']
