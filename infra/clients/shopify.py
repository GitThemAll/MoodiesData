import os
import requests
from dotenv import load_dotenv

class ShopifyClient:
    def __init__(self):
        load_dotenv()
        self.shop_name= os.getenv("shopify_shop_name")
        self.access_token = os.getenv("shopify_access_token")
        self.api_version = os.getenv("shopify_api_v", "2025-04")
        self.base_url = f"https://{self.shop_name}.myshopify.com/admin/api/{self.api_version}/"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    def get_orders(self):
        url = f"{self.base_url}/orders.json"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("orders", [])

    def get_shopify_response(self):
        return requests.get(self.base_url, headers=self.headers)
