from django import forms

from content.models import TeamModel


class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamModel
        fields = ['photo', 'name', 'title']
