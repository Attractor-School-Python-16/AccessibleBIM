from django import forms

from modules.models import ChapterModel


class ChaptersForm(forms.ModelForm):
    class Meta:
        model = ChapterModel
        fields = ['course', 'title', 'description', 'serial_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
