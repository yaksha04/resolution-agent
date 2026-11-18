"""
Mock database for orders and inventory.
In a real system these would be SQL/NoSQL queries.
"""

# Mock orders table
ORDERS = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "customer_name": "Aarav Sharma",
        "customer_email": "aarav@example.com",
        "item_id": "ITEM-A",
        "item_name": "Wireless Headphones",
        "order_status": "delivered",
        "eligible_for_exchange": True,
        "amount": 2499.0,
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "customer_name": "Priya Patel",
        "customer_email": "priya@example.com",
        "item_id": "ITEM-B",
        "item_name": "Smart Watch",
        "order_status": "delivered",
        "eligible_for_exchange": True,
        "amount": 8999.0,
    },
    "ORD-1003": {
        "order_id": "ORD-1003",
        "customer_name": "Rahul Verma",
        "customer_email": "rahul@example.com",
        "item_id": "ITEM-C",
        "item_name": "Bluetooth Speaker",
        "order_status": "delivered",
        "eligible_for_exchange": False,  # not eligible
        "amount": 1499.0,
    },
    "ORD-9999": {
        "order_id": "ORD-9999",
        "customer_name": "Invalid",
        "customer_email": "invalid@example.com",
        "item_id": "ITEM-X",
        "item_name": "Unknown",
        "order_status": "unknown",
        "eligible_for_exchange": False,
        "amount": 0,
    },
}

# Mock inventory table
INVENTORY = {
    "ITEM-A": {"item_id": "ITEM-A", "item_name": "Wireless Headphones", "stock": 5},
    "ITEM-B": {"item_id": "ITEM-B", "item_name": "Smart Watch", "stock": 0},      # out of stock
    "ITEM-C": {"item_id": "ITEM-C", "item_name": "Bluetooth Speaker", "stock": 12},
}


def get_order(order_id: str):
    return ORDERS.get(order_id)


def get_inventory(item_id: str):
    return INVENTORY.get(item_id)
