from django import forms

from subscription.models import SubscriptionModel


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionModel
        fields = ['course', 'price', 'discount']
