from fastapi import FastAPI, HTTPException
from fetch_orders import fetch_and_store_orders
from db_handler import get_all_orders

app = FastAPI()

@app.get("/orders")
def fetch_orders():
    """Fetch all orders from the database and trigger Shopify API fetch."""
    try:
        # Step 1: Fetch orders from Shopify and store in database
        fetch_and_store_orders()

        # Step 2: Retrieve all orders from the database
        orders = get_all_orders()

        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)