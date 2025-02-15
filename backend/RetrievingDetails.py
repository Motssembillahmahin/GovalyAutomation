from db_handler import get_all_orders

def fetch_particular_orders(search: str = None):
    """Fetch all orders with optional search filtering."""
    
    # Fetch all orders from DB
    orders = get_all_orders()

    # If no search query, return all orders
    if not search:
        return orders

    # Normalize search input
    search_lower = search.strip().lower()

    # Filter orders based on search criteria
    filtered_orders = [
        order for order in orders if 
        search_lower in str(order.get("order_name", "")).lower() or
        search_lower in str(order.get("customer_id", "")).lower() or
        search_lower in str(order.get("id", "")).lower() or
        search_lower in str(order.get("phone", "")).lower()
    ]

    return filtered_orders
