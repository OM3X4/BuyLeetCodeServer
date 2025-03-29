from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.conf import settings

# Create your views here.
@api_view(["POST"])
def get_auth_token(request):
    url = "https://accept.paymob.com/api/auth/tokens"
    response = requests.post(url, json={"api_key": settings.PAYMOB_API_KEY})

    if response.status_code == 201:
        return Response(response.json())
    return Response(response.json(), status=response.status_code)


@api_view(["POST"])
def create_order(request):
    token = request.data.get("token")
    amount = request.data.get("amount")  # Amount in cents (100 EGP = 10000)

    url = "https://accept.paymob.com/api/ecommerce/orders"
    payload = {
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": str(amount),
        "currency": "EGP",
        "items": []
    }

    response = requests.post(url, json=payload)
    return Response(response.json(), status=response.status_code)

@api_view(["POST"])
def get_payment_key(request):
    token = request.data.get("token")
    order_id = request.data.get("order_id")
    amount = request.data.get("amount")

    url = "https://accept.paymob.com/api/acceptance/payment_keys"
    payload = {
        "auth_token": token,
        "amount_cents": str(amount),
        "expiration": 3600,
        "order_id": order_id,
        "currency": "EGP",
        "integration_id": settings.PAYMOB_INTEGRATION_ID,
        "billing_data": {
            "first_name": "Omar",
            "last_name": "Emad",
            "phone_number": "01000000000",
            "email": "omar@example.com"
        }
    }

    response = requests.post(url, json=payload)
    return Response(response.json(), status=response.status_code)


