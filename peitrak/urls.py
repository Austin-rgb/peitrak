from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('register/',register, name ='register'),
    path('transactions/', CompletedTransactionListView.as_view(), name='completed_transactions'),
    path('send/',send,name='send'),
    path('send/<str:account_no>/<int:amount>/',send_to,name= 'send_to'),
    path('pending_transactions/',PendingTransactionListView.as_view(),name='pending_transactions'),
    path('pending_transactions/receive/<str:transaction_id>/',receive,name='receive_transaction'),
    path('pending_transactions/reject/<str:transaction_id>/',reject,name='reject_transaction'),
    path('pending_transactions/cancel/<str:transaction_id>/',cancel,name='cancel_transaction')
]
