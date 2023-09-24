from django import forms

from step.models import TextModel


class TextForm(forms.ModelForm):
    class Meta:
        model = TextModel
        fields = '__all__'
        labels = {
            'text_title': 'Введите наименование текста',
            'text_description': 'Введите описание текста',
            'content': 'Заполните текст занятия',
        }
