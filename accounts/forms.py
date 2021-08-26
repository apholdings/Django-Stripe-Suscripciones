from django import forms


class CancelSubscriptionForm(forms.Form):
    hidden = forms.HiddenInput()