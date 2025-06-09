from infra.clients.shopify import ShopifyClient
from domains.insights.filters.get_top_skus_metrics import compute_top_sku_stats

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