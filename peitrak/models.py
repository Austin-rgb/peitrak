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

def transaction_id():
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(10))

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
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_transactions_sent')
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_transactions_received')
    amount = FloatField ()
    sent = DateTimeField(default=datetime.now)
    
    class Meta:
        abstract = True


class CompletedTransaction(Transaction):
    received = DateTimeField(default = datetime.now)


class PendingTransaction(Transaction):
    pin = IntegerField(default =generate_pin )


class CancelledTransaction(Transaction):
    cancelled = DateTimeField (default =datetime.now)


class RejectedTransaction(Transaction):
    rejected = DateTimeField (default =datetime.now)

