from django import forms
from quiz_bim.models.test_bim import TestBim
from django.forms import widgets


class TestBimForm(forms.ModelForm):

    class Meta:
        model = TestBim
        fields = '__all__'
        labels = {
            'title': 'Тема тестирования',
            'questions_qty': 'Количество вопросов в тесте',
        }
        widgets = {
            'test_title': widgets.TextInput(attrs={'class': 'form-control'}),
            'questions_qty': widgets.NumberInput(attrs={'class': 'form-control'}),
        }
