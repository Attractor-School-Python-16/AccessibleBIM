from django import forms
from quiz_bim.models.quiz_bim import QuizBim
from django.forms import widgets


class QuizBimForm(forms.ModelForm):

    class Meta:
        model = QuizBim
        fields = '__all__'
        labels = {
            'title': 'Тема тестирования',
            'questions_qty': 'Количество вопросов в тесте',
        }
        widgets = {
            'test_title': widgets.TextInput(attrs={'class': 'form-control'}),
            'questions_qty': widgets.NumberInput(attrs={'class': 'form-control'}),
        }
