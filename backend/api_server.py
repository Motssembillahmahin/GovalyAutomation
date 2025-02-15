import sys
import os
import hmac
import hashlib
import base64
from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend directory is in Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions correctly
from db_handler import get_all_orders, update_order, insert_order_to_db
from fetch_orders import fetch_and_store_orders
from RetrievingDetails import fetch_particular_orders

# 🔹 Instead of loading from `.env`, hardcode your Shopify secret here
SHOPIFY_SECRET = ""

if not SHOPIFY_SECRET:
    print("🚨 ERROR: `SHOPIFY_SECRET` is missing! Set it in the file.")
    raise ValueError("SHOPIFY_SECRET is required")

print(f"✅ `SHOPIFY_SECRET` Loaded Successfully: {SHOPIFY_SECRET[:5]}********")


app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Govaly Automation API"}

@app.get("/orders")
def fetch_orders():
    """Fetch all orders from the database and trigger Shopify API fetch."""
    try:
        fetch_and_store_orders()
        orders = get_all_orders()
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch-shopify-orders")
def fetch_particular_orders_endpoint():
    """Fetch latest orders from Shopify API"""
    try:
        orders = fetch_particular_orders()
        return {"success": True, "data": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Webhook Verification
def verify_webhook(data, hmac_header):
    """Verify Shopify webhook HMAC signature."""
    if not SHOPIFY_SECRET:
        print("🚨 `SHOPIFY_SECRET` is missing! Cannot verify webhook.")
        return False

    if not hmac_header:
        print("🚨 Missing HMAC header in request!")
        return False

    if not data:
        print("🚨 Webhook request body is empty!")
        return False

    try:
        calculated_hmac = base64.b64encode(
            hmac.new(SHOPIFY_SECRET.encode(), data, hashlib.sha256).digest()
        ).decode()

        print(f"🔍 Calculated HMAC: {calculated_hmac}")
        print(f"🔍 Received HMAC: {hmac_header}")

        if hmac.compare_digest(calculated_hmac, hmac_header):
            print("✅ Webhook verified successfully!")
            return True
        else:
            print("❌ Webhook verification failed!")
            return False

    except Exception as e:
        print(f"🚨 Webhook verification error: {e}")
        return False

@app.post("/webhook/orders")
async def shopify_order_webhook(request: Request):
    """Webhook for receiving Shopify order data and storing it in the database."""
    try:
        hmac_header = request.headers.get("X-Shopify-Hmac-Sha256")
        data = await request.body()

        # Debugging: Print incoming request
        print("📩 Incoming Webhook Headers:", dict(request.headers))
        print("📩 Raw Webhook Data:", data)

        if not verify_webhook(data, hmac_header):
            print("🚨 Webhook verification failed!")
            return HTTPException(status_code=401, detail="Unauthorized")

        order_data = await request.json()
        print(f"📦 New Order Received: {order_data.get('id')}")

        # Store order in database
        insert_order_to_db(order_data)

        return {"success": True}
    except Exception as e:
        print(f"❌ Webhook Error: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))


@app.put("/update-order/{order_id}")
def update_order_endpoint(order_id: int, address: str, phone: str):
    """Update missing Address & Phone."""
    update_order(order_id, address, phone)
    return {"message": f"Order {order_id} updated successfully!"}
