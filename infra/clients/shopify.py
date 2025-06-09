import os
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv

class ShopifyClient:
    shop_name: str = None
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
    
    def get_all_orders_since(self, start_date: str, output_file="resources\data\processed\segment\shopify_orders.csv"):
        """Fetch all orders from start_date until now, and write to CSV."""
        url = f"{self.base_url}/orders.json"
        params = {
            "status": "any",
            "limit": 250,
            "created_at_min": start_date,
            "created_at_max": datetime.utcnow().isoformat() + "Z"
        }

        orders = []
        while url:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            batch = data.get("orders", [])
            orders.extend(batch)
            print(f"Fetched {len(batch)} orders, total: {len(orders)}")

            # Handle pagination
            link_header = response.headers.get("Link", "")
            url = None
            if 'rel="next"' in link_header:
                for part in link_header.split(","):
                    if 'rel="next"' in part:
                        url = part.split(";")[0].strip()[1:-1]
                        break
            params = None  # Only include params in first request

        self.write_orders_to_csv(orders, output_file)

    def write_orders_to_csv(self, orders, filename):
        """Write selected fields from orders to a CSV file."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                'Name', 'Email', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total',
                'Discount Amount', 'Lineitem quantity', 'Lineitem name', 'Lineitem price',
                'Lineitem sku', 'Billing City', 'Billing Country', 'Payment Method', 'Id'
            ])

            for order in orders:
                shipping = order.get("shipping_address", {})
                billing = order.get("billing_address", {})
                discount = sum([float(d.get("amount", 0)) for d in order.get("discount_applications", [])])
                for item in order.get("line_items", []):
                    writer.writerow([
                        order.get("name"),
                        order.get("email"),
                        order.get("processed_at"),
                        order.get("buyer_accepts_marketing"),
                        f"{shipping.get('address1', '')}, {shipping.get('city', '')}, {shipping.get('country', '')}",
                        order.get("total_price"),
                        discount,
                        item.get("quantity"),
                        item.get("name"),
                        item.get("price"),
                        item.get("sku"),
                        billing.get("city", ""),
                        billing.get("country", ""),
                        order.get("gateway", ""),
                        order.get("id")
                    ])


    def get_shopify_response(self):
        return requests.get(self.base_url, headers=self.headers)
    
    def get_orders_between(self, start_date: str, end_date: str):
        """Fetch orders from Shopify between start_date and end_date."""
        url = f"{self.base_url}/orders.json"
        params = {
            "status": "any",
            "limit": 250,
            "created_at_min": f"{start_date}T00:00:00Z",
            "created_at_max": f"{end_date}T23:59:59Z"
        }

        orders = []
        while url:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            batch = data.get("orders", [])
            orders.extend(batch)

            # Handle pagination
            link_header = response.headers.get("Link", "")
            url = None
            if 'rel="next"' in link_header:
                for part in link_header.split(","):
                    if 'rel="next"' in part:
                        url = part.split(";")[0].strip()[1:-1]
                        break
            params = None  # Only include params on the first request

        return orders
