from collections import defaultdict
from decimal import Decimal
import pandas as pd

def order_count_per_discount_code(orders: list[dict]) -> dict[str, int]:
    count_by_code = defaultdict(int)

    for order in orders:
        discount_codes = order.get("discount_codes", [])
        for discount in discount_codes:
            code = discount.get("code")
            if code:
                count_by_code[code] += 1

    return dict(count_by_code)

#can be used if data are called from shopify directly with filtering option on date
def revenue_per_discount_code(orders: list[dict]) -> dict[str, float]:
    revenue_map = defaultdict(Decimal)

    for order in orders:
        total_price = Decimal(order.get("total_price", "0"))
        discount_codes = order.get("discount_codes", [])
        for discount in discount_codes:
            code = discount.get("code")
            if code:
                revenue_map[code] += total_price

    return {code: float(revenue) for code, revenue in revenue_map.items()}

def order_count_per_discount_code(orders: list[dict]) -> dict[str, int]:
    count_by_code = defaultdict(int)

    for order in orders:
        discount_codes = order.get("discount_codes", [])
        for discount in discount_codes:
            code = discount.get("code")
            if code:
                count_by_code[code] += 1

    return dict(count_by_code)