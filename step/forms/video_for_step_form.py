from django import forms
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _

from step.models import VideoModel

CONTENTTYPES = ['video/mp4',
                'video/webm',
                'audio/ogg']


class VideoForStepForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['video_title', 'video_description', 'video_file']
        labels = {
            'title': _("Enter video's title"),
            'video_description': _("Enter video's description"),
            'video_file': _("Upload video file"),
        }

    def clean_video_file(self):
        current_file = self.cleaned_data.get("video_file", False)
        if not isinstance(current_file, FieldFile) and current_file:
            if current_file.content_type in CONTENTTYPES:
                if current_file.size <= 2097152000:
                    return current_file
                else:
                    raise forms.ValidationError(_("Uploaded file has to be no more than 2 GB"))
            else:
                raise forms.ValidationError(_("Only MP4, WebM and OGG formats allowed"))
        else:
            return current_file
