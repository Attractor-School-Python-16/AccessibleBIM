from django import forms

from modules.models import CourseTargetModel


class CourseTargetForm(forms.ModelForm):
    class Meta:
        model = CourseTargetModel
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
