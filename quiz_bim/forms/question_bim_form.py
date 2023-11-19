from django import forms
from django.utils.translation import gettext_lazy as _
from quiz_bim.models.question_bim import QuestionBim


class QuestionBimForm(forms.ModelForm):

    class Meta:
        model = QuestionBim
        fields = ['title']
        labels = {
            'title': _('Enter question'),
        }
