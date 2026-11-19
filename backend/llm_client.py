import json
import os
import urllib.request
from ai_tools import PRODUCTION_TOOLS, execute_tool

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434"
)

MODEL_NAME = os.getenv("LLM_MODEL", "qwen3:8b")


def ask_llm(question: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are AI Production Copilot, "
                    "an assistant for manufacturing operations. "
                    "Answer in Polish. "
                    "Do not invent production data."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False,
        "think": False
    }

    request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    return result["message"]["content"]

def ask_llm_with_tools(question: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are AI Production Copilot. "
                    "Use available tools when you need real production data. "
                    "Never invent inventory numbers."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "tools": PRODUCTION_TOOLS,
        "stream": False,
        "think": False
    }

    request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    return result["message"]

def ask_llm_with_tool_execution(question: str) -> str:
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

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": PRODUCTION_TOOLS,
        "stream": False,
        "think": False
    }

    request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    assistant_message = result["message"]
    tool_calls = assistant_message.get("tool_calls", [])

    if not tool_calls:
        return assistant_message.get("content", "")

    # Zachowujemy wiadomość modelu z żądaniem narzędzia.
    messages.append(assistant_message)

    MAX_TOOL_CALLS = 3

    if len(tool_calls) > MAX_TOOL_CALLS:
        raise ValueError("Too many tool calls requested")
    
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
            "content": json.dumps(tool_result, ensure_ascii=False)
        })

    # Drugie zapytanie: model otrzymuje wynik narzędzia.
    final_payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "think": False
    }

    final_request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/chat",
        data=json.dumps(final_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(final_request, timeout=120) as response:
        final_result = json.load(response)

    return final_result["message"]["content"]