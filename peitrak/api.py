from peewee import IntegrityError
from peewee import DoesNotExist

from .models import Transaction
from .models import PendingTransaction
from .models import RejectedTransaction
from .models import CancelledTransaction
from .models import Account

from .payment import Mpesa
from .payment import PayPal
from .payment import Wallet as Inwallet

from .exceptions import *

payment_methods = dict(
    mpesa=Mpesa,
    paypal =PayPal,
    wallet =Inwallet
)

class Wallet:     
    def __init__(self,account:str,payment_method):
        try:
            self.account = Account.get(Account.account_no==account)
        except DoesNotExist:
            raise InvalidAccount("Account does not exist")
        self.payment_method = payment_methods[payment_method](account)
          
    def deposit(self,amount:float):
        return self.payment_method.receive(amount).to_account(self.account.account_no)
        
    def withdraw(self,amount:float):
        if self.account.balance > amount:
            self.payment_method.send(amount)
            return True
        return False
    
    @staticmethod
    def create(account_no:str):
        account = Account(account_no=account_no)
        account.save()
    

class Transact:
    def __init__(self,account_id:str,payment_method:str) -> None:
        try:
            self.account = Account.get(Account.account_no==account_id)
        
        except DoesNotExist:
            raise InvalidAccount("User error: Account doesn't exist")
        self.payment_method = payment_methods[payment_method](account_id)

    def send(self,destination: str,amount:float)->tuple[str,int]:
        self.payment_method.request(amount)
        pending_transaction = PendingTransaction(source=self.account.account_no, destination =destination, amount =amount) 
        pending_transaction.save()
        if self.payment_method.receive(amount).to_transaction(pending_transaction.id):
            return pending_transaction.id,pending_transaction.pin
        return None,None

    def receive(self,transaction_id:int,pin:int)->bool:
        pending_transaction = PendingTransaction.get(PendingTransaction.id==transaction_id)
        if pending_transaction.pin == pin:
            transaction = Transaction(
                source=pending_transaction.source,
                destination=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent
                )
                
            transaction.save()
            pending_transaction.delete_instance()
            return self.payment_method.send(transaction.amount)
        
        else:
            raise InvalidPin("User error: Incorrect transaction Pin ")

    def cancel(self,transaction_id:int)->bool:
        pending_transaction = PendingTransaction.get(PendingTransaction.id==transaction_id)
        if self.account_no==pending_transaction.source:
            cancelled_transaction = CancelledTransaction(source_id=pending_transaction.source,
                destination_id=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent)
                
            cancelled_transaction.save()
            pending_transaction.delete_instance()
            self.payment_method.send(cancelled_transaction.amount)
            return True
            
        return False 

    def reject(self,transaction_id:int)->bool:
        acc = Account.get(Account.account_no==self.account_no)
        if not acc: return False
        pending_transaction = PendingTransaction.get(PendingTransaction.id==transaction_id)
        if not pending_transaction: return False
        
        if self.account_no==pending_transaction.destination:
            acc.balance += pending_transaction.amount
            rejected_transaction = RejectedTransaction(source_id=pending_transaction.source,
                destination_id=pending_transaction.destination,
                amount=pending_transaction.amount,
                sent = pending_transaction.sent)
                
            rejected_transaction.save()
            pending_transaction.delete_instance()
            acc.save()
            return True
            
        else:
            return False
  