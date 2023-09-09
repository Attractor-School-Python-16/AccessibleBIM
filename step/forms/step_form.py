from django import forms

from step.models.step import StepModel
from step.models.text import TextModel
from step.models.video import VideoModel
from test_bim.models.test_bim import TestBim


class StepForm(forms.ModelForm):
    text = forms.ModelChoiceField(queryset=TextModel.objects.all())
    video = forms.ModelChoiceField(queryset=VideoModel.objects.all())
    test = forms.ModelChoiceField(queryset=TestBim.objects.all())
    class Meta:
        model = StepModel
        fields = '__all__'
        labels = {
            'chapter': 'Выберите этап',
            'title': 'Укажите название занятия',
            'lesson_type': 'Выберите тип занятия',
            'text': 'Выберите текст',
            'video': 'Выберите видео',
            'test': 'Выберите тест',
            'file': 'Прикрепите файл',
            'learn_time': 'Укажите продолжительность изучения материала или прохождения теста'
        }
        widgets = {
            'chapter': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.Select(attrs={'class': 'form-control'}),
            'test': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'learn_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }
