from django import forms
from django.utils.translation import gettext_lazy as _

from step.forms.text_for_step_form import TextForStepForm


class TextForm(TextForStepForm):
    def clean_text_title(self):
        title = self.cleaned_data.get('text_title')
        if not title:
            raise forms.ValidationError(_('Please enter reading title'))
        return title

    def clean_text_description(self):
        description = self.cleaned_data.get('text_description')
        if not description:
            raise forms.ValidationError(_('Please enter reading description'))
        return description

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError(_('Please enter reading content'))
        return content
