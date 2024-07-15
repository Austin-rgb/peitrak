from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .forms import SendForm
from .api import Transact

class Cancel(APIView):
    def post(self,request, *args, **kwargs):
        pass

class Send(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        form = SendForm(request.data)
        if form.is_valid():
            user = request.user
            payment_method = form.cleaned_data['payment_method']
            destination = form.cleaned_data['destination']
            amount = form.cleaned_data['amount']
            transact = Transact(user,payment_method)
            transaction, pin = transact.send(destination,amount)
            return Response({'sent':True})
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)