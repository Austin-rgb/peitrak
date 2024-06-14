from django import forms
from .models import PendingTransaction

class SendForm(forms.Form):
    destination = forms.CharField(max_length=10)
    amount = forms.FloatField()
    payment_method = forms.ChoiceField(choices=("mpesa","wallet"))

class ReceiveForm(forms.ModelForm):
    pin = forms.IntegerField(max_value=9999)