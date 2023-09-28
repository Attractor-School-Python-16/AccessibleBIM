from django import forms

from step.models import VideoModel

CONTENTTYPES = ['video/mp4',
                'video/x-msvideo']


class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = '__all__'
        labels = {
            'video_title': 'Введите наименование видео',
            'video_description': 'Введите описание видео',
            'video_file': 'Загрузите видео-файл',
        }

    def clean_video_file(self):
        current_file = self.cleaned_data.get("video_file", False)
        if current_file.content_type in CONTENTTYPES:
            return current_file
        else:
            raise forms.ValidationError("Необходимо загрузить видео в формате MP4 или AVI")
