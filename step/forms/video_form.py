from django import forms
from django.db.models.fields.files import FieldFile

from step.models import VideoModel

CONTENTTYPES = ['video/mp4',
                'video/webm',
                'audio/ogg']


class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['video_title', 'video_description', 'video_file']

    def clean_video_file(self):
        current_file = self.cleaned_data.get("video_file", False)
        if not isinstance(current_file, FieldFile) and current_file:
            if current_file.content_type in CONTENTTYPES:
                if current_file.size <= 2097152000:
                    return current_file
                else:
                    raise forms.ValidationError("Размер загружаемого файла не должен превышать 2ГБ")
            else:
                raise forms.ValidationError("Необходимо загрузить видео в формате MP4, WebM или Ogg")
        else:
            return current_file
