from django import forms
from django.utils.translation import gettext_lazy as _

from step.models.step import StepModel


class StepTextForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'text']
        labels = {
            'title': _("Enter lesson's title"),
            'learn_time': _("Enter lesson's duration (min.)"),
            'file': _("Select files"),
            'text': _("Select reading"),
        }


class StepVideoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'video']
        labels = {
            'title': _("Enter lesson's title"),
            'learn_time': _("Enter lesson's duration (min.)"),
            'file': _("Select files"),
            'video': _("Select video"),
        }


class StepQuizForm(forms.ModelForm):
    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'test']
        labels = {
            'title': _("Enter lesson's title"),
            'learn_time': _("Enter lesson's duration (min.)"),
            'quiz': _("Select test"),
        }
