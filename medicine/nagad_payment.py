import requests
from django.conf import settings

class NagadPayment:
    def __init__(self):
        self.base_url = settings.NAGAD_BASE_URL
        self.merchant_id = settings.NAGAD_MERCHANT_ID
        self.public_key_path = settings.NAGAD_PUBLIC_KEY_PATH
        self.private_key_path = settings.NAGAD_PRIVATE_KEY_PATH

    def initialize_checkout(self, order_id):
        url = f"{self.base_url}/remote-payment-gateway-1.0/api/dfs/check-out/initialize/{self.merchant_id}/{order_id}"

        # Load the keys
        with open(self.public_key_path, 'r') as file:
            public_key = file.read()

        with open(self.private_key_path, 'r') as file:
            private_key = file.read()

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "orderId": order_id,
            "merchantId": self.merchant_id,
            # Add other required data if needed
        }

        # Send request to initialize payment
        response = requests.post(url, json=data, headers=headers, verify=False)
        return response.json()

    def complete_checkout(self, payment_reference_id):
        url = f"{self.base_url}/remote-payment-gateway-1.0/api/dfs/check-out/complete/{payment_reference_id}"
        
        response = requests.get(url)
        return response.json()

    def verify_payment(self, payment_reference_id):
        url = f"{self.base_url}/remote-payment-gateway-1.0/api/dfs/verify/payment/{payment_reference_id}"
        
        response = requests.get(url)
        return response.json()
