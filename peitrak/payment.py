from .models import Account
from .models import PendingTransaction, Withdrawal, Deposit,PendingDeposit


class AccountMngr:     
    def __init__(self,user):
        try:
            self.account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            raise Exception("Account does not exist")
        
          
    def deposit(self,payment):
        payment.to_account(self.account.user)
        
    def withdraw(self,amount:float):
        if self.account.balance > amount:
            self.account.balance-=amount 
            self.account.save()  
            withdraw = Withdrawal(
                user= self.account.user,
                amount=amount,
            )
            withdraw.save()
            return Payment(amount)
        return False

class Payment: 
    def __init__(self, amount,account=None, transaction=None) -> None:
        self.amount=0
        if account: 
            if account.balance >= amount: 
                account.balance-=amount 
                account.save()
                self.amount = amount 
            else:
                raise Exception ("Insufficient balance ")
                
        elif transaction: 
            if transaction.amount >= amount: 
                transaction.delete()
                self.amount = amount 
     

    def to_account(self,user ): 
        account=Account.objects.get(user=user)
        account.balance+=self.amount
        account.save()
        del(self)
        return True

    def to_transaction(self,transaction):
        transaction.amount = self.amount
        transaction.save()
        del(self)
        return True

class PaymentMethod:
    """
    General class for handling transactions
    """
    def __init__(self,user) -> None:
        self.account = Account.objects.get(user=user)

    def receive(self,amount:float)->Payment:
        pending = PendingDeposit(
            user=self.account.user,
            amount=amount 
        )
        pending.save()
        return Payment(amount, transaction =pending)
    
    def request(self,amount:float):
        return None
    
    def send(self,payment:Payment)->bool:
        withdraw = Withdrawal(
            amount=payment.amount,
            user=self.account.user
        )
        withdraw. save()
        payment.to_transaction(withdraw)
        return True
        
    
class Mpesa(PaymentMethod):
    """
    Class for handling transactions over mpesa
    """
    def __init__(self,user) -> None:
        super().__init__(user)

    def receive(self,amount:float)->Payment:
        return super().receive(amount)
    
    def request(self,amount:float):
        return None
    
    def send(self,amount:float)->bool:
        return super().send(amount)
    

class PayPal(PaymentMethod):
    """
    Class for handling transactions in PayPal 
    """
    def __init__(self,user) -> None:
        super().__init__(user=user)

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
    def __init__(self,user) -> None:
        super().__init__(user)
        
    def receive(self,amount:float)->bool:
        if self.account.balance >=amount:
            return Payment(amount,self.account)
        return False
    
    def request(self,amount:float):
        return super().request(amount)
    
    def send(self,payment)->bool:
        payment.to_account(self.account.user)
