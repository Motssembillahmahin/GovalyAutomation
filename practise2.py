import hmac
import hashlib
import base64

SHOPIFY_SECRET = "732bc1dc5bcc31450e06d37c247bb72f72b9a475234a4a0559330e4918620064"
payload = '{"test": "data"}'  # Example payload

calculated_hmac = base64.b64encode(
    hmac.new(SHOPIFY_SECRET.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).digest()
).decode('utf-8')

print("Your HMAC:", calculated_hmac)
