import json

from llm_client import chat_completion
from ai_tools import PRODUCTION_TOOLS, execute_tool


MAX_TOOL_CALLS = 3


def get_ai_response(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are AI Production Copilot. "
                "Answer in Polish. "
                "Use tools when the user asks about real production data. "
                "Base production numbers only on tool results. "
                "Never invent inventory numbers."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # 1. Pytamy model, czy potrzebuje narzędzia
    assistant_message = chat_completion(
        messages=messages,
        tools=PRODUCTION_TOOLS
    )

    tool_calls = assistant_message.get("tool_calls", [])

    # 2. Jeśli model nie potrzebuje narzędzia,
    # zwracamy jego odpowiedź
    if not tool_calls:
        return assistant_message.get("content", "")

    # 3. Sprawdzamy limit wywołań
    if len(tool_calls) > MAX_TOOL_CALLS:
        raise ValueError("Too many tool calls")

    messages.append(assistant_message)

    # 4. Wykonujemy dozwolone narzędzia
    for tool_call in tool_calls:
        function = tool_call["function"]
        tool_name = function["name"]
        arguments = function.get("arguments", {})

        if not isinstance(arguments, dict):
            raise ValueError("Invalid tool arguments")

        tool_result = execute_tool(tool_name, arguments)

        messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": json.dumps(
                tool_result,
                ensure_ascii=False
            )
        })

    # 5. Przekazujemy wyniki narzędzi modelowi
    final_message = chat_completion(messages=messages)

    return final_message.get("content", "")