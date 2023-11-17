from django import forms
from django.utils.translation import gettext_lazy as _

class SubscriptionUserDeleteForm(forms.Form):
    delete = forms.CharField(max_length=100, required=False, label=_("Unsubscribe"))
