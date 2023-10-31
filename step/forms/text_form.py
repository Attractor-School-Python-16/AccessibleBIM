from django import forms
from django_summernote.widgets import SummernoteWidget
from step.models import TextModel


class TextForm(forms.ModelForm):
    class Meta:
        model = TextModel
        fields = ['text_title', 'text_description', 'content']
        labels = {
            'text_title': 'Введите наименование лекции',
            'text_description': 'Укажите описание лекции',
            'content': 'Содержание лекции',
        }
        widgets = {
            'text_description': SummernoteWidget(),
            'content': SummernoteWidget(),
        }
