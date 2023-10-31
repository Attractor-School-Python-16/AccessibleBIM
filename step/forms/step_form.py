from django import forms
from step.models.step import StepModel


class StepTextForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'text']
        labels = {
            'title': 'Введите наименование занятия',
            'learn_time': 'Укажите продолжительность занятия',
            'file': 'Выберите файлы',
            'text': 'Выберите лекцию',
        }


class StepVideoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'file', 'video']
        labels = {
            'title': 'Введите наименование занятия',
            'learn_time': 'Укажите продолжительность занятия',
            'file': 'Выберите файлы',
            'video': 'Выберите видео',
        }


class StepQuizForm(forms.ModelForm):
    class Meta:
        model = StepModel
        fields = ['title', 'learn_time', 'test']
        labels = {
            'title': 'Введите наименование занятия',
            'learn_time': 'Укажите продолжительность занятия',
            'video': 'Выберите тест',
        }
