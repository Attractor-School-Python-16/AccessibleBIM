from django import forms

from step.models import VideoModel


class VideoModelForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['title', 'description', 'video_file']
        labels = {
            'title': 'Введите наименование видео',
            'description': 'Введите описание видео',
            'video_file': 'Загрузите видео-файл',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
