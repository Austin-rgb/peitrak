from datetime import datetime
import string
import random
from random import randint
from django.db.models import AutoField
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import DateTimeField
from django.db.models import IntegerField
from django.db.models import CharField 
from django.db.models import SqliteDatabase


database = SqliteDatabase('wallet')
def generate_pin():
    return randint(1000,9999)

def transaction_id():
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(10))

class Account(Model):
    account_no = CharField(max_length = 32,primary_key = True)
    balance = FloatField(default=0.0)

class BaseTransaction(Model):
    id = CharField(max_length=10,default=transaction_id)
    source = CharField(max_length = 32)
    destination = CharField(max_length = 32)
    amount = FloatField ()
    sent = DateTimeField()


class Transaction(BaseTransaction):
    received = DateTimeField(default = datetime.now)


class PendingTransaction(BaseTransaction):
    sent = DateTimeField(default = datetime.now)
    pin = IntegerField(default =generate_pin )


class CancelledTransaction(BaseTransaction):
    cancelled = DateTimeField (default =datetime.now)


class RejectedTransaction(BaseTransaction):
    rejected = DateTimeField (default =datetime.now)

