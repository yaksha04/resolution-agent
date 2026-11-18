"""
Safe tool dispatcher + whitelist registry.
"""

from tools import lookup_order, check_inventory, process_refund, send_notification

# Whitelist registry
TOOL_REGISTRY = {
    "lookup_order": lookup_order,
    "check_inventory": check_inventory,
    "process_refund": process_refund,
    "send_notification": send_notification,
}


def dispatch_tool(tool_name: str, arguments: dict) -> dict:
    """
    Safe dispatcher. Only executes tools that are in the registry.
    """
    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' is not authorized. Available tools: {list(TOOL_REGISTRY.keys())}",
            "data": None,
        }
    try:
        func = TOOL_REGISTRY[tool_name]
        result = func(**arguments)
        return result
    except TypeError as e:
        return {
            "success": False,
            "error": f"Invalid arguments for tool '{tool_name}': {str(e)}",
            "data": None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Tool execution error: {str(e)}",
            "data": None,
        }
