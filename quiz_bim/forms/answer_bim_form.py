from django import forms
from django.utils.translation import gettext_lazy as _

from quiz_bim.models.answer_bim import AnswerBim


class AnswerBimForm(forms.ModelForm):

    class Meta:
        model = AnswerBim
        fields = ['answer', 'is_correct']
        labels = {
            'answer': _('Answer'),
            'is_correct': _('Right answer'),

        }

