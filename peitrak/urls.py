from django.urls import path, include
from rest_framework.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('api',include('peitrak.api_urls')),
    path('register/',register, name ='register'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('send/',send,name='send'),
    path('send/<str:request_id>/',send_to,name= 'send_to'),
    path('profile',profile, name='profile'),
    path('pending_transactions/receive/<str:transaction_id>/',receive,name='receive_transaction'),
    path('pending_transactions/reject/<str:transaction_id>/',reject,name='reject_transaction'),
    path('pending_transactions/cancel/<str:transaction_id>/',cancel,name='cancel_transaction'),

]
