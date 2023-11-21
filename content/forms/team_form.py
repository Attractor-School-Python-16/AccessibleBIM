from django import forms
from django.utils.translation import gettext_lazy as _
from content.models import TeamModel


class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamModel
        fields = ['photo', 'name', 'title']
        labels = {
            'photo': _('Photo'),
            'name': _("Member's name"),
            'title': _("Member's title")
        }
