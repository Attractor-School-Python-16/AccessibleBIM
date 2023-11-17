from django import forms
from django.utils.translation import gettext_lazy as _

class SubscriptionUserAddForm(forms.Form):
    button = forms.CharField(max_length=100, required=False, label=_("Grant subscription"))
