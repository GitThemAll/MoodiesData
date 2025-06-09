from collections import defaultdict
from decimal import Decimal

def compute_top_sku_stats(orders: list[dict], top_skus: dict[str, str]) -> list[dict]:
    sku_stats = defaultdict(lambda: {
        "sku": "", "name": "", "num_customers": set(), "units_sold": 0, "revenue": Decimal("0.00")
    })

    for order in orders:
        email = order.get("email")
        line_items = order.get("line_items", [])

        for item in line_items:
            sku = item.get("sku")
            if sku not in top_skus:
                continue

            quantity = int(item.get("quantity", 0))
            price = Decimal(str(item.get("price", "0")))

            stats = sku_stats[sku]
            stats["sku"] = sku
            stats["name"] = top_skus[sku]
            stats["units_sold"] += quantity
            stats["revenue"] += quantity * price
            if email:
                stats["num_customers"].add(email)

    # Format and convert to list
    return [
        {
            "Lineitem sku": stat["sku"],
            "Name": stat["name"],
            "num_customers": len(stat["num_customers"]),
            "units_sold": stat["units_sold"],
            "revenue": float(round(stat["revenue"], 2))
        }
        for stat in sku_stats.values()
    ]

#calculate revenu per sku using shopfy client
def revenue_per_sku(orders: list[dict]) -> dict[str, float]:
    sku_revenue = defaultdict(Decimal)

    for order in orders:
        for item in order.get("line_items", []):
            sku = item.get("sku")
            quantity = item.get("quantity", 0)
            price = item.get("price", "0")

            if sku:
                try:
                    revenue = Decimal(str(price)) * Decimal(quantity)
                    sku_revenue[sku] += revenue
                except:
                    continue  # skip malformed values

    return {sku: float(amount) for sku, amount in sku_revenue.items()}

def order_count_per_sku(orders: list[dict]) -> dict[str, int]:
    sku_counts = defaultdict(int)

    for order in orders:
        seen_skus = set() #set type indicated to avoind duplicating sku count
        for item in order.get("line_items", []):
            sku = item.get("sku")
            if sku and sku not in seen_skus:
                sku_counts[sku] += 1
                seen_skus.add(sku)

    return dict(sku_counts)