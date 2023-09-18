from django import forms
from django.forms import widgets
from test_bim.models.answer_bim import AnswerBim


class AnswerBimForm(forms.ModelForm):

    class Meta:
        model = AnswerBim
        fields = ['answer', 'is_correct']
        labels = {
            'answer': 'Ответ на вопрос',
            'is_correct': 'Верный ответ',

        }
        widgets = {
            'answer': widgets.TextInput(attrs={'class': 'form-control'}),
            'is_correct': widgets.Select(attrs={'class': 'form-select'}),
        }
