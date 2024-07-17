from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api_views import *
urlpatterns=[
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('send/',Send.as_view(),name='send'),
    path('receive/',Receive.as_view(),name='receive'),
    path('cancel/',Cancel.as_view(),name='cancel')
]