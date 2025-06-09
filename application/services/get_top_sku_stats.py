from infra.clients.shopify import ShopifyClient
from domains.insights.filters.get_top_skus_metrics import compute_top_sku_stats
from domains.insights.filters.get_top_skus_metrics import revenue_per_sku
from domains.insights.filters.get_top_skus_metrics import order_count_per_sku
import os 
import json

class SkuStatsService:
    def __init__(self):
        self.shopify = ShopifyClient()

    def get_top_sku_metrics(self):
        orders = self.shopify.get_orders()
        top_skus = {
            "MS-006": "boyshort super dames",
            "YM-006": "boyshort gemiddeld-zwaar meiden",
            "YH-006": "boyshort hevig meiden",
            "MM-008": "hipster lace",
            "ML-009": "string",
            "SY-001": "menstruatie zwemkleding klassieke bikini meiden",
            "SM-001": "menstruatie zwemkleding klassieke bikini dames",
            "SM-003": "menstruatie zwemkleding cheeky",
            "EM-010": "everyday hiphugger laser-cut",
            "EM-008": "everyday hipster lace"
        }
        return compute_top_sku_stats(orders, top_skus)
    
    #shopify function to get skus from shopify api 
    def get_revenue_per_sku(self):
        try:
            #used lines to call shopify client
            # orders = self.shopify.get_orders_between(start, end)
            # result = revenue_per_sku(orders)

            file_path = os.path.join("resources", "data", "processed", "insights", "skus_revenu.json")

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
        
    def get_order_count_per_sku(self):
        try:
            # orders = self.shopify.get_orders_between(start, end)            
            # result = order_count_per_sku(orders)

            file_path = os.path.join("resources", "data", "processed", "insights", "order_count_per_sku.json")
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
        
    