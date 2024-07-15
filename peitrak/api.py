from datetime import datetime
from django.contrib.auth.models import User
from .models import Transaction
from .models import Account

from .payment import Mpesa
from .payment import PayPal
from .payment import TransactionPayment, PaymentMethod
from .payment import Wallet as Inwallet

from .exceptions import *

payment_methods:dict[str,PaymentMethod] = {
    '1':Mpesa,
    '2' :Inwallet,
    '3' :PayPal
}

def validate_username(username):
    try:
        user = User.objects.get(username =username)
        return True
    except:
        pass

def validate_transaction_id(transaction_id):
    try:
        transaction = Transaction.objects.get (id=transaction_id)
        return True 
    except Exception as e:
        print(e)

def validate_pin(pin,transaction_id):
    try:
        transaction = Transaction.objects.get (id=transaction_id,pin=pin )
        return True 
    except Exception as e:
        print(e)
def validate_payment(user,payment_method,amount):
    try:
        user = User.objects.get(username=user)
        payment_method = payment_methods[payment_method](user)
        payment = payment_method.receive(amount)
        if payment:
            payment.to_account(user)
            return True
    except Exception as e:
        print(e)
class Wallet:     
    def __init__(self,user,payment_method):
        try:
            self.account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            raise InvalidAccount("Account does not exist")
        self.payment_method:PaymentMethod = payment_methods[payment_method](user)
          
    def deposit(self,amount:float):
        return self.payment_method.receive(amount).to_account(self.account.account_no)
        
    def withdraw(self,amount:float):
        if self.account.balance > amount:
            self.payment_method.send(amount)
            return True
        return False
    
    @staticmethod
    def create(user):
        account = Account(user=user)
        account.save()
    

class Transact:
    def __init__(self,user:str,payment_method:str) -> None:
        try:
            self.account = Account.objects.get(user=user)
        
        except Account.DoesNotExist:
            raise InvalidAccount("User error: Account doesn't exist")
        self.payment_method:PaymentMethod = payment_methods[payment_method](user)

    def send(self,destination: str,amount:float)->tuple[str,int]:
        self.payment_method.request(amount)
        destination = User.objects.get(username=destination)
        transaction = Transaction(source=self.account.user, destination =destination, amount =amount) 
        transaction.save()
        payment = self.payment_method.receive(amount)
        if payment:
            payment.to_transaction(transaction)
            return transaction.id,transaction.pin
        return payment

    def receive(self,transaction_id:int,pin:int)->bool:
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.pin == pin and transaction.can_receive():
            transaction.receive()
            payment = TransactionPayment (transaction)
            return self.payment_method.send(payment)
        
        else:
            raise InvalidPin("User error: Incorrect transaction Pin ")

    def cancel(self,transaction_id:int)->bool:
        transaction = Transaction.objects.get(id=transaction_id)
        if self.account.user==transaction.source:
            transaction.cancel()
            payment = TransactionPayment(transaction)
            self.payment_method.send(payment)
            return True
            
        return False 

    def reject(self,transaction_id:int)->bool:
        transaction = Transaction.objects.get(id=transaction_id)
        if self.account.user==transaction.destination:
            transaction.reject()
            payment = TransactionPayment(transaction)
            return payment.to_account(transaction.source)
            
        else:
            return False
  
