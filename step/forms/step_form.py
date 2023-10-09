from django import forms
from step.models.step import StepModel


class StepTextForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = [('', 'Пусто')] + list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'text']


class StepVideoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = [('', 'Пусто')] + list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'video']


class StepQuizForm(forms.ModelForm):
    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'test']
