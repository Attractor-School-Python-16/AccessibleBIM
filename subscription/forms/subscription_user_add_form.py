from django import forms


class SubscriptionUserAddForm(forms.Form):
    button = forms.CharField(max_length=100, required=False, label="Выдать подписку")
