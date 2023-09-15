from django import forms

from subscription.models import SubscriptionModel


class SubscriptionUserAddForm(forms.ModelForm):
    class Meta:
        model = SubscriptionModel
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
