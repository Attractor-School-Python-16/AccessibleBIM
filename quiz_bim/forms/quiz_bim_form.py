from django import forms
from django.utils.translation import gettext_lazy as _
from quiz_bim.forms.quiz_bim_for_step_form import QuizBimForStepForm


class QuizBimForm(QuizBimForStepForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError(_('Please enter title'))
        return title
