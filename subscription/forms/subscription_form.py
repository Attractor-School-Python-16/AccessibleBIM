from django import forms

from subscription.models import SubscriptionModel


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionModel
        fields = ['course', 'price', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
