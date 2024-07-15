from .models import Account
from .models import Transaction, Withdrawal, Deposit,PendingDeposit


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
    def to_account(self,user ):
        try: 
            account=Account.objects.get(user=user)
            account.balance+=self.amount
            account.save()
            del(self)
            return True
        except Exception as e:
            print(e)

    def to_transaction(self,transaction):
        transaction.amount = self.amount
        transaction.save()
        del(self)
        return True
class TransactionPayment(Payment):
    def __init__(self,transaction:Transaction) -> None:
        if transaction.amount >= transaction.amount: 
            transaction.delete()
            self.amount = transaction.amount

class AccountPayment(Payment):
    def __init__(self,account, amount) -> None:
        self.amount=0
        if account.balance >= amount: 
            account.balance-=amount 
            account.save()
            self.amount = amount 
        else:
            raise Exception ("Insufficient balance ")
                
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
        return TransactionPayment(pending)
    
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
            return AccountPayment(amount=amount,account=self.account)
        return False
    
    def request(self,amount:float):
        return super().request(amount)
    
    def send(self,payment)->bool:
        payment.to_account(self.account.user)
