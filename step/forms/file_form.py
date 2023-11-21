from django import forms
from django.utils.translation import gettext_lazy as _

from step.forms.file_for_step_form import FileForStepForm


class FileForm(FileForStepForm):
    def clean_file_title(self):
        title = self.cleaned_data.get('file_title')
        if not title:
            raise forms.ValidationError(_("Title is mandatory for uploading a file"))
        return title

    def clean_lesson_file(self):
        super().clean_lesson_file()
        lesson_file = self.cleaned_data.get("lesson_file", False)
        if not lesson_file:
            raise forms.ValidationError(_("Please upload a file"))
        return lesson_file
