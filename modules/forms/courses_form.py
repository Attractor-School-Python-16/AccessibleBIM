from django import forms

from modules.models import CourseModel


class CoursesForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = ['title', 'description', 'image', 'learnTime', 'module_id', 'courseTarget_id', 'teachers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
