from django import forms


class SubscriptionUserDeleteForm(forms.Form):
    delete = forms.CharField(max_length=100, required=False, label="Отключить подписку")
