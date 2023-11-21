from django import forms
from django.utils.translation import gettext_lazy as _

from step.forms.video_for_step_form import VideoForStepForm


class VideoForm(VideoForStepForm):
    def clean_video_file(self):
        file = super().clean_video_file()
        if not file:
            raise forms.ValidationError(_('Please upload video file'))
        return file

    def clean_video_title(self):
        title = self.cleaned_data.get('video_title')
        if not title:
            raise forms.ValidationError(_('Please enter video title'))
        return title
