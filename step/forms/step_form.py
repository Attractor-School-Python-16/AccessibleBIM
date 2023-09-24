from django import forms

from step.models import FileModel
from step.models.step import StepModel
from step.models.text import TextModel
from step.models.video import VideoModel
from quiz_bim.models.quiz_bim import QuizBim


class StepForm(forms.ModelForm):
    text = forms.ModelChoiceField(queryset=TextModel.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    video = forms.ModelChoiceField(queryset=VideoModel.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    test = forms.ModelChoiceField(queryset=QuizBim.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.ModelMultipleChoiceField(queryset=FileModel.objects.all(), initial=None, required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].choices = [('', 'Пусто')] + list(self.fields['file'].choices)

    class Meta:
        model = StepModel
        fields = ['title', 'lesson_type', 'text', 'video', 'test', 'file', 'learn_time']
        labels = {
            'title': 'Укажите название занятия',
            'lesson_type': 'Выберите тип занятия',
            'text': 'Выберите текст',
            'video': 'Выберите видео',
            'test': 'Выберите тест',
            'file': 'Прикрепите файл',
            'learn_time': 'Укажите продолжительность изучения материала или прохождения теста',
            'serial_number': 'Укажите порядковый номер занятия'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
            'learn_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'serial_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
