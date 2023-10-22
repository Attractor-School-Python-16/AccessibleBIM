from django import forms
from django_summernote.widgets import SummernoteWidget
from step.models import TextModel


class TextForm(forms.ModelForm):
    class Meta:
        model = TextModel
        fields = ['text_title', 'text_description', 'content']

        widgets = {
            'text_description': SummernoteWidget(),
            'content': SummernoteWidget(),
        }
