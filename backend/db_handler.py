import pyodbc
import os

# 🔹 Database Configuration
DB_SERVER = os.getenv("DB_SERVER", "l")
DB_NAME = os.getenv("DB_NAME", "G")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD}",
            autocommit=True
        )
        return conn
    except pyodbc.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None


def create_orders_table():
    """Create the orders table if it doesn't exist."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'orders')
            CREATE TABLE orders (
                Order_ID BIGINT PRIMARY KEY,
                Customer_ID BIGINT,
                Order_Name NVARCHAR(50),
                Total_Amount DECIMAL(18, 2),
                Financial_Status NVARCHAR(50),
                Fulfillment_Status NVARCHAR(50),
                Vendor_Names NVARCHAR(MAX),
                Payment_Gateway NVARCHAR(255),
                Note NVARCHAR(MAX),
                Address NVARCHAR(MAX),
                Phone_Number NVARCHAR(20),
                Created_At DATETIME DEFAULT GETDATE()
            )
        """)
        print("✅ Orders table created/verified")
    except pyodbc.Error as e:
        print(f"❌ Table creation failed: {e}")
    finally:
        conn.close()


def insert_order_to_db(order):
    """Insert or update a single order into the database using MERGE."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Extract Address Information
        shipping_address = order.get("shipping_address", {})
        address_parts = [
            shipping_address.get("address1", ""),
            shipping_address.get("address2", ""),
            shipping_address.get("city", ""),
            shipping_address.get("province", ""),
            shipping_address.get("country", ""),
        ]
        formatted_address = ", ".join(filter(None, address_parts))

        # Extract phone number (prioritize shipping address phone)
        phone = shipping_address.get("phone") or order.get("customer", {}).get("phone", "N/A")

        # Extract Other Order Details
        params = (
            order.get("id"),  # Order_ID
            order.get("customer", {}).get("id"),  # Customer_ID
            order.get("name", "Unknown"),  # Order_Name
            float(order.get("total_price", 0)),  # Total_Amount
            order.get("financial_status", "N/A"),  # Financial_Status
            order.get("fulfillment_status", "N/A"),  # Fulfillment_Status
            ", ".join(set(item.get("vendor", "N/A") for item in order.get("line_items", []))),  # Vendor_Names
            ", ".join(order.get("payment_gateway_names", ["N/A"])),  # Payment_Gateway
            order.get("note", ""),  # Note
            formatted_address,  # Address
            phone  # Phone_Number
        )

        # Debugging: Print the parameter tuple
        print("📦 Storing Order:", params)

        # 🔹 Use MERGE to Insert or Update
        cursor.execute("""
            MERGE INTO orders AS target
            USING (SELECT ? AS Order_ID, ? AS Customer_ID, ? AS Order_Name, ? AS Total_Amount, 
                          ? AS Financial_Status, ? AS Fulfillment_Status, ? AS Vendor_Names, 
                          ? AS Payment_Gateway, ? AS Note, ? AS Address, ? AS Phone_Number) AS source
            ON target.Order_ID = source.Order_ID
            WHEN MATCHED THEN
                UPDATE SET 
                    Customer_ID = source.Customer_ID,
                    Order_Name = source.Order_Name,
                    Total_Amount = source.Total_Amount,
                    Financial_Status = source.Financial_Status,
                    Fulfillment_Status = source.Fulfillment_Status,
                    Vendor_Names = source.Vendor_Names,
                    Payment_Gateway = source.Payment_Gateway,
                    Note = source.Note,
                    Address = source.Address,
                    Phone_Number = source.Phone_Number
            WHEN NOT MATCHED THEN
                INSERT (Order_ID, Customer_ID, Order_Name, Total_Amount, Financial_Status, 
                        Fulfillment_Status, Vendor_Names, Payment_Gateway, Note, Address, Phone_Number)
                VALUES (source.Order_ID, source.Customer_ID, source.Order_Name, source.Total_Amount, 
                        source.Financial_Status, source.Fulfillment_Status, source.Vendor_Names, 
                        source.Payment_Gateway, source.Note, source.Address, source.Phone_Number);
        """, params)

        conn.commit()
        print(f"✅ Order {order.get('id')} inserted/updated successfully.")

    except pyodbc.Error as e:
        print(f"❌ Failed to insert/update order {order.get('id')}: {e}")
    finally:
        conn.close()


def get_all_orders():
    """Fetch all orders from the database."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return [
            {
                "id": o[0],
                "customer_id": o[1],
                "order_name": o[2],
                "total_amount": o[3],
                "financial_status": o[4],
                "fulfillment_status": o[5],
                "vendor_names": o[6],
                "payment_gateway": o[7],
                "note": o[8],
                "address": o[9],
                "phone": o[10]
            }
            for o in orders
        ]
    except pyodbc.Error as e:
        print(f"❌ Failed to fetch orders: {e}")
        return []
    finally:
        conn.close()


def update_order(order_id, address, phone):
    """Update an order's address and phone number in the database."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders 
            SET Address = ?, Phone_Number = ? 
            WHERE Order_ID = ?
        """, (address, phone, order_id))
        conn.commit()
        print(f"✅ Order {order_id} updated successfully.")
    except pyodbc.Error as e:
        print(f"❌ Update failed: {e}")
    finally:
        conn.close()
