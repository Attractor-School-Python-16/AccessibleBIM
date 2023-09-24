from django import forms

from step.models import VideoModel


class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = '__all__'
        labels = {
            'video_title': 'Введите наименование видео',
            'video_description': 'Введите описание видео',
            'video_file': 'Загрузите видео-файл',
        }
