from domains.insights.filters.discount_code_metrics import order_count_per_discount_code
from infra.clients.shopify import ShopifyClient

class DiscountCodeService:
    def __init__(self):
        self.shopify = ShopifyClient()

    def get_discount_code_usage_metrics(self):
        orders = self.shopify.get_orders()
        return order_count_per_discount_code(orders)