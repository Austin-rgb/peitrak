from django.contrib.auth.models import User
from .models import CompletedTransaction
from .models import PendingTransaction
from .models import RejectedTransaction
from .models import CancelledTransaction
from .models import Account

from .payment import Mpesa
from .payment import PayPal
from .payment import Payment, PaymentMethod
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
        pending_transaction = PendingTransaction.objects.get (id=transaction_id)
        return True 
    except Exception as e:
        print(e)

def validate_pin(pin,transaction_id):
    try:
        pending_transaction = PendingTransaction.objects.get (id=transaction_id,pin=pin )
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
        pending_transaction = PendingTransaction(source=self.account.user, destination =destination, amount =amount) 
        pending_transaction.save()
        payment = self.payment_method.receive(amount)
        if payment:
            payment.to_transaction(pending_transaction)
            return pending_transaction.id,pending_transaction.pin
        return payment

    def receive(self,transaction_id:int,pin:int)->bool:
        pending_transaction = PendingTransaction.objects.get(id=transaction_id)
        if pending_transaction.pin == pin:
            transaction = CompletedTransaction(
                source=pending_transaction.source,
                destination=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent
                )
                
            transaction.save()
            payment = Payment (transaction.amount, transaction=pending_transaction)
            return self.payment_method.send(payment)
        
        else:
            raise InvalidPin("User error: Incorrect transaction Pin ")

    def cancel(self,transaction_id:int)->bool:
        pending_transaction = PendingTransaction.objects.get(id=transaction_id)
        if self.account.user==pending_transaction.source:
            cancelled_transaction = CancelledTransaction(source=pending_transaction.source,
                destination=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent)
                
            cancelled_transaction.save()
            payment = Payment(pending_transaction.amount,transaction =pending_transaction)
            self.payment_method.send(payment)
            return True
            
        return False 

    def reject(self,transaction_id:int)->bool:
        pending_transaction = PendingTransaction.objects.get(id=transaction_id)
        if self.account.user==pending_transaction.destination:
            self.account.balance += pending_transaction.amount
            rejected_transaction = RejectedTransaction(source=pending_transaction.source,
                destination=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent)
                
            rejected_transaction.save()
            pending_transaction.delete()
            self.account.save()
            return True
            
        else:
            return False
  
