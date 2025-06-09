from domains.insights.filters.discount_code_metrics import order_count_per_discount_code
from infra.clients.shopify import ShopifyClient
from domains.insights.filters.discount_code_metrics import revenue_per_discount_code
import pandas as pd
import json 
import os 

class DiscountCodeService:
    def __init__(self):
        self.shopify = ShopifyClient()

    def get_discount_code_usage_metrics(self):
        orders = self.shopify.get_orders()
        return order_count_per_discount_code(orders)
    
    #function used to get data on certain date (self, start_date: str, end_date: str):
    # def get_discount_code_revenue(self, start_date: str, end_date: str):

    def get_discount_code_revenue(self):
        try:
            ##this line gets orders directly from shopify api 
            #orders = self.shopify.get_orders_between(start_date, end_date)

            file_path = os.path.join("resources", "data", "processed", "insights", "discount_code_revenu.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # result = revenue_per_discount_code(orders)
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_discount_code_order_count(self):
        try:
            #next lines is used to call shopify api and get needed isnights on certain dates from 01-mar-2024 -> 01-jun-2025
            # orders = self.shopify.get_orders_between(start_date, end_date)
            # result = order_count_per_discount_code(orders)

            file_path = os.path.join("resources", "data", "processed", "insights", "discount_code_item_nb.json")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }