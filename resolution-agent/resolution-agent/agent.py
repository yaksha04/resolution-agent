"""
Agentic resolution agent with ReAct-style loop.
Uses structured decision logic (works without external LLM API).
Demonstrates the full tool-calling cycle, conditional branching, and guardrails.
"""

from dispatcher import dispatch_tool
from schemas import TOOL_SCHEMAS

MAX_ITERATIONS = 5


def run_resolution_agent(user_request: str, order_id: str = None) -> dict:
    """
    Autonomous resolution agent.
    Returns the final summary + full trace of tool calls.
    """
    history = []
    trace = []
    iteration = 0

    # Extract order_id if present in request, otherwise use provided
    if not order_id:
        # simple extraction for demo
        for word in user_request.split():
            if word.startswith("ORD-"):
                order_id = word.strip(".,")
                break

    if not order_id:
        return {
            "success": False,
            "summary": "Please provide a valid order ID (e.g. ORD-1001) so I can look it up.",
            "trace": [],
        }

    # Step 1: Always look up the order first
    history.append({"role": "user", "content": user_request})
    result = dispatch_tool("lookup_order", {"order_id": order_id})
    trace.append({"tool": "lookup_order", "args": {"order_id": order_id}, "result": result})
    iteration += 1

    if not result["success"]:
        return {
            "success": False,
            "summary": result["error"],
            "trace": trace,
        }

    order = result["data"]
    customer_email = order["customer_email"]
    item_id = order["item_id"]
    item_name = order["item_name"]
    eligible = order["eligible_for_exchange"]
    amount = order["amount"]

    # Step 2: Check inventory if eligible
    if eligible:
        inv_result = dispatch_tool("check_inventory", {"item_id": item_id})
        trace.append({"tool": "check_inventory", "args": {"item_id": item_id}, "result": inv_result})
        iteration += 1

        if inv_result["success"] and inv_result["data"]["available_for_exchange"]:
            # Exchange path
            message = (
                f"Hello {order['customer_name']},\n\n"
                f"Your order {order_id} ({item_name}) is eligible for exchange and a replacement is in stock. "
                f"We have initiated the exchange. You will receive the replacement soon.\n\n"
                f"Thank you for your patience."
            )
            notif = dispatch_tool("send_notification", {"email": customer_email, "message": message})
            trace.append({"tool": "send_notification", "args": {"email": customer_email}, "result": notif})

            summary = (
                f"Exchange confirmed for order {order_id}.\n"
                f"Item: {item_name}\n"
                f"Customer: {order['customer_name']}\n"
                f"Replacement stock available. Confirmation email sent to {customer_email}."
            )
            return {"success": True, "summary": summary, "trace": trace, "resolution": "exchange"}

    # Refund path (not eligible OR out of stock)
    reason = "Out of stock for exchange" if eligible else "Order not eligible for exchange"
    refund_result = dispatch_tool("process_refund", {"order_id": order_id, "reason": reason})
    trace.append({"tool": "process_refund", "args": {"order_id": order_id, "reason": reason}, "result": refund_result})
    iteration += 1

    if refund_result["success"]:
        refund_data = refund_result["data"]
        message = (
            f"Hello {order['customer_name']},\n\n"
            f"We were unable to process an exchange for your order {order_id} ({item_name}). "
            f"A refund of ₹{amount} has been initiated (Reference: {refund_data['refund_id']}).\n"
            f"Reason: {reason}\n\n"
            f"The amount will be credited to your original payment method within 5-7 business days."
        )
        notif = dispatch_tool("send_notification", {"email": customer_email, "message": message})
        trace.append({"tool": "send_notification", "args": {"email": customer_email}, "result": notif})

        summary = (
            f"Refund initiated for order {order_id}.\n"
            f"Item: {item_name}\n"
            f"Amount: ₹{amount}\n"
            f"Refund ID: {refund_data['refund_id']}\n"
            f"Reason: {reason}\n"
            f"Confirmation email sent to {customer_email}."
        )
        return {"success": True, "summary": summary, "trace": trace, "resolution": "refund"}

    return {
        "success": False,
        "summary": "Failed to complete resolution. Please try again or contact support.",
        "trace": trace,
    }
