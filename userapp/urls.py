from django.urls import path

from userapp.apps import UserappConfig
from userapp.views import PaymentListAPIView, UserListAPIView

app_name = UserappConfig.name

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('user/', UserListAPIView.as_view(), name='user_list')
]
