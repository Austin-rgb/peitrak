from django.contrib import admin
from django.urls import path

from .views import send, receive

urlpatterns = [
    path('admin/', admin.site.urls),
]