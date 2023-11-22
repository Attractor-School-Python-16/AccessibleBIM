from django import forms
from django.utils.translation import gettext_lazy as _
from content.models import PartnerModel


class PartnerForm(forms.ModelForm):
    class Meta:
        model = PartnerModel
        fields = ['title', 'image']
