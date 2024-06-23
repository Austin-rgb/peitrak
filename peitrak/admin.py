from django.contrib import admin
from  .models import Account, PendingTransaction, CompletedTransaction, CancelledTransaction, RejectedTransaction
# Register your models here.
admin.register(Account)
admin.register(PendingTransaction)
admin.register(CompletedTransaction)
admin.register(CancelledTransaction)
admin.register(RejectedTransaction)