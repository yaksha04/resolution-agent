"""
Functional tools the agent can call.
Each returns structured data with success/error status.
"""

from mock_db import get_order, get_inventory
import uuid


def lookup_order(order_id: str) -> dict:
    """Look up an order by ID."""
    order = get_order(order_id)
    if not order:
        return {
            "success": False,
            "error": f"Order '{order_id}' not found. Please verify the order ID.",
            "data": None,
        }
    return {
        "success": True,
        "error": None,
        "data": order,
    }


def check_inventory(item_id: str) -> dict:
    """Check real-time warehouse stock for an item."""
    inv = get_inventory(item_id)
    if not inv:
        return {
            "success": False,
            "error": f"Item '{item_id}' not found in inventory.",
            "data": None,
        }
    available = inv["stock"] > 0
    return {
        "success": True,
        "error": None,
        "data": {
            "item_id": item_id,
            "item_name": inv["item_name"],
            "stock": inv["stock"],
            "available_for_exchange": available,
        },
    }


def process_refund(order_id: str, reason: str) -> dict:
    """Issue a refund for an order."""
    order = get_order(order_id)
    if not order:
        return {
            "success": False,
            "error": f"Cannot refund: order '{order_id}' not found.",
            "data": None,
        }
    refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
    return {
        "success": True,
        "error": None,
        "data": {
            "refund_id": refund_id,
            "order_id": order_id,
            "amount": order["amount"],
            "reason": reason,
            "status": "refund_initiated",
        },
    }


def send_notification(email: str, message: str) -> dict:
    """Send a confirmation email to the customer (mock)."""
    if not email or "@" not in email:
        return {
            "success": False,
            "error": "Invalid email address.",
            "data": None,
        }
    return {
        "success": True,
        "error": None,
        "data": {
            "email": email,
            "message": message,
            "status": "sent",
            "timestamp": "2026-11-18T14:30:00Z",
        },
    }
