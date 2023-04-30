import requests
from django.conf import settings


def get_paypal_token():
    if settings.PAYPAL_MODE == "sandbox":
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    else:
        url = "https://api-m.paypal.com/v1/oauth2/token"

    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, auth=auth, headers=headers, data=data)
    response.raise_for_status()
    access_token = response.json()["access_token"]
    return access_token


def create_paypal_product(name):
    """createa a paypal product"""
    if settings.PAYPAL_MODE == "sandbox":
        url = "https://api-m.sandbox.paypal.com/v1/catalogs/products"
    else:
        url = "https://api-m.paypal.com/v1/catalogs/products"

    access_token = get_paypal_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    data = {
        "name": name,
        "description": "Transmister subscription for transacribing voice recordgins",
        "type": "DIGITAL",
        "category": "SOFTWARE",
        "home_url": "https://transmister.com",
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def create_paypal_plan(product_id: str, plan_name: str):
    """Create product sbuscription plan"""
    if settings.PAYPAL_MODE == "sandbox":
        url = "https://api-m.sandbox.paypal.com/v1/billing/plans"
    else:
        url = "https://api-m.paypal.com/v1/billing/plans"

    access_token = get_paypal_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    data = {
        "product_id": product_id,
        "name": plan_name,
        "description": "Monthly subscription for upgraded Transmister plan",
        "status": "ACTIVE",
        "billing_cycles": [
            {
                "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {"value": "5", "currency_code": "USD"}
                },
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {"value": "0", "currency_code": "USD"},
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3,
        },
        "taxes": {"percentage": "0", "inclusive": True},
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def create_paypal_order(request, amount, currency, return_url, cancel_url):
    if settings.PAYPAL_MODE == "sandbox":
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    else:
        url = "https://api-m.paypal.com/v2/checkout/orders"

    access_token = get_paypal_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": amount,
                }
            }
        ],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def capture_paypal_order(token):
    if settings.PAYPAL_MODE == "sandbox":
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{token}/capture"
    else:
        url = f"https://api-m.paypal.com/v2/checkout/orders/{token}/capture"

    access_token = get_paypal_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()
