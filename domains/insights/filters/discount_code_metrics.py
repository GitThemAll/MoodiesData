from collections import defaultdict
from decimal import Decimal

def order_count_per_discount_code(orders: list[dict]) -> dict[str, int]:
    count_by_code = defaultdict(int)

    for order in orders:
        discount_codes = order.get("discount_codes", [])
        for discount in discount_codes:
            code = discount.get("code")
            if code:
                count_by_code[code] += 1

    return dict(count_by_code)