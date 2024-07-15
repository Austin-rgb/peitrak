from django.urls import path
from rest_framework.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api_urls import *
url_patterns=[
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh')

]