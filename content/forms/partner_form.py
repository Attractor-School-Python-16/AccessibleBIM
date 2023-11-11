from django import forms

from content.models import PartnerModel


class PartnerForm(forms.ModelForm):
    class Meta:
        model = PartnerModel
        fields = ['title', 'image']
