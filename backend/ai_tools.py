from inventory_service import get_production_context
from rag_service import search_knowledge

MAX_KNOWLEDGE_QUERY_LENGTH = 1000

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
    },
    {
        "type": "function",
        "function": {
            "name": "search_company_knowledge",
            "description": (
                "Search internal manufacturing documentation, "
                "company procedures, quality control instructions, "
                "warehouse procedures and CNC safety guidelines. "
                "Use this tool when the user asks about company "
                "rules, procedures or how to handle production issues."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A focused search query in the user's language."
                        )
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }   
]

def search_company_knowledge(query: str) -> dict:
    results = search_knowledge(query)

    documents = []

    for item in results:
        payload = item["payload"]

        documents.append({
            "source": payload["source"],
            "text": payload["text"],
            "chunk_index": payload["chunk_index"],
            "score": round(item["score"], 4)
        })

    return {
        "found": bool(documents),
        "documents": documents
    }

def execute_tool(tool_name: str, arguments: dict) -> dict:

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a dictionary")

    if tool_name == "get_production_context":

        if arguments:
            raise ValueError(
                "get_production_context does not accept arguments"
            )

        return get_production_context()

    if tool_name == "search_company_knowledge":

        if set(arguments.keys()) != {"query"}:
            raise ValueError(
                "search_company_knowledge requires only query"
            )

        query = arguments["query"]

        if not isinstance(query, str):
            raise ValueError("Query must be a string")

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty")

        if len(query) > MAX_KNOWLEDGE_QUERY_LENGTH:
            raise ValueError("Query is too long")

        return search_company_knowledge(query)

    raise ValueError(f"Unknown tool: {tool_name}")