from django import forms
from quiz_bim.models.quiz_bim import QuizBim
from django.forms import widgets


class QuizBimForm(forms.ModelForm):

    class Meta:
        model = QuizBim
        fields = ['title', 'questions_qty']
        widgets = {
            'questions_qty': forms.NumberInput(attrs={'value': 0}),
        }