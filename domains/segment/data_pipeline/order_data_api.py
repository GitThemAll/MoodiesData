import requests
import csv
from datetime import datetime

# Config
SHOP = "your-store.myshopify.com"
API_VERSION = "2024-07"
ACCESS_TOKEN = "your-access-token"

# Date range
start_date = "2024-03-01T00:00:00Z"
end_date = datetime.utcnow().isoformat() + "Z"

# API setup
url = f"https://{SHOP}/admin/api/{API_VERSION}/orders.json"
headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}
params = {
    "status": "any",
    "limit": 250,
    "created_at_min": start_date,
    "created_at_max": end_date
}

orders = []
while url:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    orders.extend(data.get("orders", []))
    print(f"Fetched {len(data.get('orders', []))} orders, total: {len(orders)}")

    # Pagination
    link_header = response.headers.get("Link", "")
    url = None
    if 'rel="next"' in link_header:
        for part in link_header.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip()[1:-1]
                break
    params = None

# Save to CSV
filename = "shopify_orders_detailed.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Custom columns
    writer.writerow([
        'Name', 'Email', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total',
        'Discount Amount', 'Lineitem quantity', 'Lineitem name', 'Lineitem price',
        'Lineitem sku', 'Billing City', 'Billing Country', 'Payment Method', 'Id'
    ])

    for order in orders:
        # Flatten line items - write a row per item
        for item in order.get("line_items", []):
            shipping_address = order.get("shipping_address", {})
            billing_address = order.get("billing_address", {})
            discount = sum([float(d.get("amount", 0)) for d in order.get("discount_applications", [])])
            
            writer.writerow([
                order.get("name"),
                order.get("email"),
                order.get("processed_at"),  # Paid at
                order.get("buyer_accepts_marketing"),
                f"{shipping_address.get('address1', '')}, {shipping_address.get('city', '')}, {shipping_address.get('country', '')}",
                order.get("total_price"),
                discount,
                item.get("quantity"),
                item.get("name"),
                item.get("price"),
                item.get("sku"),
                billing_address.get("city", ""),
                billing_address.get("country", ""),
                order.get("gateway", ""),  # Payment Method
                order.get("id")
            ])

print(f"\n✅ Saved detailed order export to: {filename}")
