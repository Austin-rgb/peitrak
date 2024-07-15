from datetime import datetime
import string
import random
from random import randint
from django.db import models
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import DateTimeField
from django.db.models import IntegerField
from django.db.models import CharField 
from django.contrib.auth.models import User

def generate_pin():
    return randint(1000,9999)

def random_string(length=4):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def transaction_id():
    return random_string(10)

def request_id():
    return random_string(32)

class Account(Model):
    user = ForeignKey(User,on_delete=models.CASCADE)
    balance = FloatField(default=0.0)

class Update(Model):
    user = models.ForeignKey (User,on_delete =models.CASCADE )
    amount = FloatField ()
    time = DateTimeField (default =datetime.now )
    class Meta: 
        abstract = True

class Withdrawal (Update):
    pass

class Deposit (Update):
    pass

class PendingWithdrawal(Update):
    pass

class PendingDeposit(Update):
    pass

class Transaction(Model):
    id = models.CharField(max_length=10,default=transaction_id,primary_key=True)
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_transactions_sent')
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_transactions_received')
    amount = FloatField (default=.0)
    sent = models.BooleanField(default=True)
    pin = IntegerField(default =generate_pin )
    received = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now=True)
    received_on = models.DateTimeField(null=True)
    cancelled_on = models.DateTimeField(null=True)
    rejected_on = models.DateTimeField(null=True)
    
    def receive(self):
        if not self.received:
            self.received = True
            self.received_on = datetime.now()
            self.save()

    def reject(self):
        if not self.rejected:
            self.rejected = True
            self.rejected_on = datetime.now()
            self.save()

    def cancel(self):
        if not self.cancel:
            self.cancelled = True
            self.cancelled_on = datetime.now()
            self.save()

    def can_receive(self):
        return not (self.received or self.rejected or self.cancelled)



class Request(models.Model):
    id = CharField(max_length=32,default=request_id,primary_key=True)
    destination = ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)