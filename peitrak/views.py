
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import SendForm, ReceiveForm
from .api import Transact, Wallet


@login_required
def profile(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        account = None
    
    completed_transactions = CompletedTransaction.objects.filter(source=user) | CompletedTransaction.objects.filter(destination=user)
    pending_transactions = PendingTransaction.objects.filter(source=user) | PendingTransaction.objects.filter(destination=user)
    
    context = {
        'account': account,
        'completed_transactions': completed_transactions,
        'pending_transactions': pending_transactions
    }
    return render(request, 'accounts/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Wallet.create(request.user)
            return redirect('send')
    else:
        form = UserCreationForm()
    return render(request, 'peitrak/register.html', {'form': form})


class TransactionListView(LoginRequiredMixin,ListView):
    paginate_by = 10
    context_object_name = 'transactions'

    def get_queryset(self):
        user = self.request.user
        query_set = self.model.objects.filter(source=user) | self.model.objects.filter(destination=user)
        query_set.order_by('-sent')
        return query_set


class CompletedTransactionListView(TransactionListView):
    model = CompletedTransaction 
    template_name = 'peitrak/completed_transactions.html'
    

class PendingTransactionListView(TransactionListView):
    model = PendingTransaction
    template_name = 'peitrak/pending_transactions.html'
    
    
class CancelledTransactionListView(TransactionListView):
    model = CancelledTransaction
    template_name = 'peitrak/cancelled_transactions.html'
    
    
class RejectedTransactionListView(TransactionListView):
    model = RejectedTransaction
    template_name = 'peitrak/rejected_transactions_list.html'
    

@login_required
def send(request):
    if request.method == 'POST':
        form = SendForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            payment_method = form.cleaned_data['payment_method']
            destination = form.cleaned_data['destination']
            amount = form.cleaned_data['amount']
            transact = Transact(user,payment_method)

            transaction, pin = transact.send(destination,amount)
            context = {}
            context['transaction_id'] = transaction
            context['pin'] = pin
            return render(request, 'peitrak/send_success.html',context)

    else:
        form = SendForm()
    return render(request, 'peitrak/send.html', {'form': form})

@login_required 
def send_to(request, account_no, amount):
    context = {}
    context['amount']=amount
    context['destination']=account_no
    if request.method == 'POST':
        form = SendForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            payment_method = form.cleaned_data['payment_method']
            destination = form.cleaned_data['destination']
            amount = form.cleaned_data['amount']
            transact = Transact(user,payment_method)
            transaction, pin = transact.send(destination,amount)
            context['transaction_id'] = transaction
            context['pin'] = pin
            next_ = request.GET.get('next')
            if next_:
                redirect(next_)
            return render(request, 'peitrak/send_success.html',context)

    else:
        
        form = SendForm (initial=context)
        context['form']=form
    return render(request, 'peitrak/send.html', context)


def start_closing_transaction(request,transaction_id ):
    transact = None
    form = None
    if request.method == 'POST':
        form = ReceiveForm(request.POST)
        if form.is_valid():
            user = request.user
            transact = Transact(user,form.cleaned_data['payment_method'])

    else:
        form = ReceiveForm(initial=dict(transaction_id=transaction_id))

    return form, transact

@login_required
def receive(request,transaction_id):
    form, transact = start_closing_transaction(request,transaction_id )
    if transact:
        if transact.receive(transaction_id, form.cleaned_data ['pin']):
            return redirect('completed_transactions')
        
    return render(request, 'peitrak/receive.html', {'form': form})

@login_required
def cancel(request,transaction_id):
    form, transact = start_closing_transaction(request,transaction_id)
    if transact:
        if transact.cancel(transaction_id):
            return redirect('completed_transactions')
    
    return render(request, 'peitrak/cancel.html', {'form': form})

@login_required
def reject(request,transaction_id):
    transact = Transact(request.user,'1')
    transact.reject(transaction_id)
    return redirect ('pending_transactions')
