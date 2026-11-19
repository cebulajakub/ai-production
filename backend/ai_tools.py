from inventory_service import get_production_context

PRODUCTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_production_context",
            "description": (
                "Get current manufacturing inventory shortages, "
                "product demand, available stock and shortage priorities. "
                "Use this tool when the user asks about production risks, "
                "inventory shortages or material availability."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def execute_tool(tool_name: str, arguments: dict):
    if tool_name == "get_production_context":
        if arguments:
            raise ValueError("This tool does not accept arguments")

        return get_production_context()

    raise ValueError(f"Unknown tool: {tool_name}")