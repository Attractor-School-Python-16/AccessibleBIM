from django import forms

from quiz_bim.models.quiz_bim import QuizBim


class QuizBimForStepForm(forms.ModelForm):

    class Meta:
        model = QuizBim
        fields = ['title']
        widgets = {
            'questions_qty': forms.NumberInput(attrs={'value': 0}),
        }
