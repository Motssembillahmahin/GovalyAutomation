import requests
from db_handler import create_orders_table, insert_order_to_db

SHOPIFY_STORE = "govalybd.myshopify.com"
API_KEY = ""
API_VERSION = "2024-01"

def fetch_and_store_orders():
    """Fetch orders from Shopify and store them in the database."""
    url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/orders.json?status=any"
    headers = {
        "X-Shopify-Access-Token": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        orders = response.json().get('orders', [])
        print(f"📦 Retrieved {len(orders)} orders from Shopify")

        # Ensure the orders table exists
        create_orders_table()

        # Insert each order into the database
        for order in orders:
            insert_order_to_db(order)
    else:
        print(f"❌ Failed to fetch orders: {response.status_code} - {response.text}")
