"""
Tool schemas (declarative contracts) the LLM/agent sees.
"""

TOOL_SCHEMAS = [
    {
        "name": "lookup_order",
        "description": "Look up order details including customer name, item, status, and exchange eligibility. Use this first when a customer reports an issue.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique order identifier (e.g. ORD-1001)",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "check_inventory",
        "description": "Check real-time warehouse stock to see if a replacement unit is available for exchange.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "string",
                    "description": "The item identifier from the order (e.g. ITEM-A)",
                }
            },
            "required": ["item_id"],
        },
    },
    {
        "name": "process_refund",
        "description": "Issue a financial refund to the customer's original payment method when a replacement is not available or the order is ineligible for exchange.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order identifier to refund",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the refund (e.g. 'Out of stock for exchange')",
                },
            },
            "required": ["order_id", "reason"],
        },
    },
    {
        "name": "send_notification",
        "description": "Send an official confirmation email to the customer summarizing the resolution.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Customer email address",
                },
                "message": {
                    "type": "string",
                    "description": "The confirmation message body",
                },
            },
            "required": ["email", "message"],
        },
    },
]
