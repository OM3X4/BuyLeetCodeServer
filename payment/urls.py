from django.urls import path
from .views import get_auth_token, create_order, get_payment_key

urlpatterns = [
    path("get_token/", get_auth_token, name="get_auth_token"),
    path("create_order/", create_order, name="create_order"),
    path("get_payment_key/", get_payment_key, name="get_payment_key"),
]
