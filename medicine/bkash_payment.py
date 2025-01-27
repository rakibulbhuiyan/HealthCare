import requests
from django.conf import settings

class BkashPayment:
    def __init__(self):
        self.base_url = settings.BKASH_BASE_URL
        self.app_key = settings.BKASH_APP_KEY
        self.app_secret = settings.BKASH_APP_SECRET
    
    def get_access_token(self):
        url = f"{self.base_url}/checkout/token/grant"
        headers={
            "Content-Type": "application/json",
            "username": self.app_key,
            "password": self.app_secret,
        }
        response = response.post(url, headers=headers)
        data = response.data()
        if response.status_code == 200 and  "id_token" in data:
            return data['id_token']
        else:
            raise Exception("Failed to get access token")
    
    def initialize_checkout(self, amount, invoice_number):
        access_token = self.get_access_token()
        url = f"{self.base_url}/checkout/payment/create"
        headers = {
            "Content-Type": "application/json",
            "Authorization": access_token,
            "X-APP-Key": self.app_key,
        }
        data = {
            "amount": str(amount),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": invoice_number,
        }
        response = response.post(url, json= data, headers=headers)
        return response.json()
    
    def execute_payment(self,payment_id):
        access_token=self.get_access_token()
        url=f"{self.base_url}/checkout/payment/execute/{payment_id}"
        headers={
            "Content-Type": "application/json",
            "Authorization": access_token,
            "X-APP-Key": self.app_key,
        }
        response = response.post(url,headers = headers)
        return response.json()
    
    def verify_payment(self,payment_id):
        access_token=self.get_access_token()
        url=f"{self.base_url}/checkout/payment/execute/{payment_id}"
        headers={
            "Content-Type": "application/json",
            "Authorization": access_token,
            "X-APP-Key": self.app_key,
        }
        response = response.get(url,headers = headers)
        return response.json()

