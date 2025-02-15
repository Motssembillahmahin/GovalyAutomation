import os
import hmac
import hashlib
import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get Shopify Secret Key from .env
SHOPIFY_SECRET = os.getenv("SHOPIFY_SECRET")
if not SHOPIFY_SECRET:
    raise ValueError("SHOPIFY_SECRET is not set in .env file!")

def verify_webhook(data, hmac_header):
    """Verify Shopify webhook authenticity using HMAC-SHA256."""
    calculated_hmac = base64.b64encode(
        hmac.new(SHOPIFY_SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    ).decode('utf-8')
    
    return hmac.compare_digest(calculated_hmac, hmac_header)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming Shopify webhooks."""
    data = request.get_data()
    hmac_header = request.headers.get("X-Shopify-Hmac-SHA256")

    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 400

    if verify_webhook(data, hmac_header):
        return jsonify({"message": "Webhook verified successfully!"}), 200
    else:
        return jsonify({"error": "Invalid webhook"}), 401

if __name__ == "__main__":
    app.run(port=5000, debug=True)
