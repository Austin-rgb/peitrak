from .models import Account
from .models import PendingTransaction

class Payment: 
    def __init__(self, amount) -> None:
        self.amount = amount 

    def to_account(self,account ): 
        account=Account.get(Account.account_no==account)
        account.balance+=self.amount
        account.save()
        del(self)
        return True

    def to_transaction(self,transaction):
        transaction = PendingTransaction.get(PendingTransaction.id==transaction)
        transaction.amount = self.amount
        transaction.save()
        del(self)
        return True

class PaymentMethod:
    """
    General class for handling transactions
    """
    def __init__(self,account_no) -> None:
        self.account = Account.get(Account.account_no==account_no)

    def receive(self,amount:float)->Payment:
        return Payment(amount)
    
    def request(self,amount:float):
        return None
    
    def send(self,amount:float)->bool:
        self.account.balance -= amount
        self.account.save()
        return True
    
class Mpesa(PaymentMethod):
    """
    Class for handling transactions over mpesa
    """
    def __init__(self,account_no) -> None:
        self.acocunt_no = account_no

    def receive(self,amount:float)->Payment:
        return super().receive(amount)
    
    def request(self,source:str,amount:float):
        return None
    
    def send(self,amount:float)->bool:
        return super().send(amount)
    

class PayPal(PaymentMethod):
    """
    Class for handling transactions in PayPal 
    """
    def __init__(self,account_no) -> None:
        self.account_no = account_no

    def receive(self,amount:float)->bool:
        return super().receive(amount)
    
    def request(self,source:str,amount:float):
        return None
    
    def send(self,amount:float)->bool:
        return super().send(amount)
    

class Wallet(PaymentMethod):
    """
    Class for handling payments in peitrak wallet
    """
    def __init__(self,account_no) -> None:
        super().__init__(account_no)
    def receive(self,amount:float)->bool:
        if self.account.balance >=amount:
            self.account.balance -= amount
            self.account.save()
            return Payment(amount)
        return False
    
    def request(self,amount:float):
        return super().request(amount)
    
    def send(self,amount:float)->bool:
        self.account.balance += amount
        self.account.save()
        return True