from django.urls import path
from .views import TelegramConnectView

urlpatterns = [
    path('telegram/connect/', TelegramConnectView.as_view(), name='telegram-connect'),
]
