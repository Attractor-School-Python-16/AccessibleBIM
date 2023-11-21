from django import forms

from modules.models import CourseModel


class CoursesByModuleForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = ['title', 'description', 'image', 'learnTime', 'courseTarget_id', 'language', 'teachers']


class CoursesStandAloneForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = ["module_id", 'title', 'description', 'image', 'learnTime', 'courseTarget_id', 'language', 'teachers']
