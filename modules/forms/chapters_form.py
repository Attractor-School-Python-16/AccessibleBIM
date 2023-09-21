from django import forms
from django_summernote.widgets import SummernoteWidget

from modules.models import ChapterModel


class ChaptersForm(forms.ModelForm):
    class Meta:
        model = ChapterModel
        fields = ['course', 'title', 'description', 'serial_number']
        widgets = {
            'title': SummernoteWidget(),
            'description': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field not in ["title", "description"]:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
