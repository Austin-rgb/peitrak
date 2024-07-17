from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .api import validate_pin, validate_transaction_id, validate_username, validate_payment

class TransactionForm(forms.Form):
    payment_method = forms.ChoiceField(choices=(('1',"mpesa"),('2',"wallet")))


class SendForm(TransactionForm):
    destination = forms.CharField(max_length=10)
    amount = forms.FloatField()
    def __init__(self,*args,user=None,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.user = user
    def clean(self) -> dict[str, Any]:
        clean_data = super().clean()
        destination = clean_data.get('destination')
        amount = clean_data.get('amount')
        payment_method = clean_data.get('payment_method')
        if not validate_username(destination):
            self.add_error('destination','Invalid destination username')

        if not validate_payment(self.user,payment_method,amount):
            self.add_error('amount', 'Insufficient payment')

        else:
            clean_data['payment_method']='2'

        return clean_data

class CancelForm(TransactionForm):
    transaction_id = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super().clean()
        transaction = cleaned_data.get('transaction_id')

        if not validate_transaction_id(transaction):
            self.add_error('transaction_id','Invalid transaction_id')

        return cleaned_data

class ReceiveForm(CancelForm):
    pin = forms.IntegerField(max_value=9999)
    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        transaction = cleaned_data.get('transaction_id')
        # PIN validation logic
        if not validate_pin(pin,transaction):
            self.add_error('pin', 'The provided PIN is incorrect.')

        return cleaned_data
