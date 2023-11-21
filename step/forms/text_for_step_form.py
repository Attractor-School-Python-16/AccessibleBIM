from django import forms
from django.utils.translation import gettext_lazy as _

from django_summernote.widgets import SummernoteWidget

from step.models import TextModel


class TextForStepForm(forms.ModelForm):
    class Meta:
        model = TextModel
        fields = ['text_title', 'text_description', 'content']
        labels = {
            'text_title': _("Enter reading's title"),
            'text_description': _("Enter reading's description"),
            'content': _("Content"),
        }
        widgets = {
            'text_description': SummernoteWidget(),
            'content': SummernoteWidget(),
        }
