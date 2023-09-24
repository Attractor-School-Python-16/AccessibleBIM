from django import forms
from django.forms import widgets
from quiz_bim.models.question_bim import QuestionBim


class QuestionBimForm(forms.ModelForm):

    class Meta:
        model = QuestionBim
        fields = ['title']
        labels = {
            'title': 'Введите вопрос',
        }
