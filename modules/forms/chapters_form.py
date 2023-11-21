from django import forms

from modules.models import ChapterModel


class ChaptersForm(forms.ModelForm):
    class Meta:
        model = ChapterModel
        fields = ['title', 'description']
