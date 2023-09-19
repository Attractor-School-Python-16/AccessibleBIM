from django import forms

from modules.models import ChapterModel
from step.models import FileModel
from step.models.step import StepModel
from step.models.text import TextModel
from step.models.video import VideoModel
from quiz_bim.models.test_bim import TestBim


class StepForm(forms.ModelForm):
    chapter = forms.ModelChoiceField(queryset=ChapterModel.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    text = forms.ModelChoiceField(queryset=TextModel.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    video = forms.ModelChoiceField(queryset=VideoModel.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    test = forms.ModelChoiceField(queryset=TestBim.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.ModelMultipleChoiceField(queryset=FileModel.objects.all(), initial=None, required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

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
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
            'learn_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'serial_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
