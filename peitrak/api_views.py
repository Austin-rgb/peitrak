from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .forms import SendForm, ReceiveForm, CancelForm,TransactionForm
from .api import Transact


class AuthtView(APIView):
    permission_classes = [IsAuthenticated]

class Reusable1(AuthtView):
    def start_transaction(self, request):
        form = TransactionForm(request.data)
        if form.is_valid():
            user = request.user
            payment_method = form.cleaned_data['payment_method']
            transact = Transact(user,payment_method)
            return transact
        
    def start_closing(self,request):
        transact = self.start_transaction(request)
        form = CancelForm(request.data)
        if form.is_valid() and transact:
            transaction_id = form.cleaned_data['transaction_id']
            return transact, transaction_id
        return None, None
        
class Receive(Reusable1):
    def post(self, request, *args, **kwargs):
        transact, transaction_id = self.start_closing(request)
        if transact:
            form = ReceiveForm(request.data)
            pin = form.cleaned_data['pin']
            transact.receive(transaction_id,pin)
            return Response({'receive':True})
        
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class Cancel(Reusable1):
    def post(self, request, *args, **kwargs):
        transact, transaction_id = self.start_closing(request)
        if transact:
            transact.cancel(transaction_id)
            return Response({'cancelled':True})
        
        return Response({'cancelled':False}, status=status.HTTP_400_BAD_REQUEST)
    
class Reject(Reusable1):
    def post(self, request, *args, **kwargs):
        transact, transaction_id = self.start_closing(request)
        if transact:
            transact.reject(transaction_id)
            return Response({'rejected':True})
        
        return Response({'rejected':False}, status=status.HTTP_400_BAD_REQUEST)

class Send(Reusable1):
    def post(self,request):
        transact = self.start_transaction(request)
        form = SendForm(request.data)
        if form.is_valid() and transact:
            destination = form.cleaned_data['destination']
            amount = form.cleaned_data['amount']
            transaction, pin = transact.send(destination,amount)
            return Response({'sent':True,'transaction_id':transaction,'pin':pin})
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)

