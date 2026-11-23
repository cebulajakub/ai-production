import json
import os
import urllib.request


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434"
)

MODEL_NAME = os.getenv("LLM_MODEL", "qwen3:8b")


def chat_completion(
    messages: list,
    tools: list | None = None
) -> dict:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "think": False
    }

    if tools is not None:
        payload["tools"] = tools

    request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(
        request,
        timeout=120
    ) as response:
        result = json.load(response)

    return result["message"]