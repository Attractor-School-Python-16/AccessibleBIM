from django import forms
from quiz_bim.models.answer_bim import AnswerBim


class AnswerBimForm(forms.ModelForm):

    class Meta:
        model = AnswerBim
        fields = ['answer', 'is_correct']
        labels = {
            'answer': 'Ответ на вопрос',
            'is_correct': 'Верный ответ',

        }

    # def clean(self):
    #     data = self.cleaned_data
    #     question = self.instance.question_bim
    #     print(question)
    #     return data