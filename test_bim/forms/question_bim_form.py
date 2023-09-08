from django import forms
from django.forms import widgets
from test_bim.models.question_bim import QuestionBim


class QuestionBimForm(forms.ModelForm):

    class Meta:
        model = QuestionBim
        fields = ['title']
        labels = {
            'title': 'Введите вопрос',
        }
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
        }
