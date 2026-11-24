import json
import os
import urllib.request

from llm_client import chat_completion


QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434"
)

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION",
    "manufacturing_knowledge"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))

RAG_SCORE_THRESHOLD = float(
    os.getenv("RAG_SCORE_THRESHOLD", "0.65")
)


def get_embedding(
    text: str,
    task: str = "search_query"
) -> list[float]:

    if task not in ("search_query", "search_document"):
        raise ValueError("Unsupported embedding task")

    if EMBEDDING_MODEL == "nomic-embed-text":
        embedding_input = f"{task}: {text}"

    elif EMBEDDING_MODEL == "bge-m3":
        embedding_input = text

    else:
        raise ValueError("Unsupported embedding model")

    payload = {
        "model": EMBEDDING_MODEL,
        "input": embedding_input
    }

    request = urllib.request.Request(
        url=f"{OLLAMA_URL}/api/embed",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    return result["embeddings"][0]


def search_knowledge(question: str) -> list[dict]:
    vector = get_embedding(
        question,
        task="search_query"
    )

    payload = {
        "vector": vector,
        "limit": RAG_TOP_K,
        "score_threshold": RAG_SCORE_THRESHOLD,
        "with_payload": True
    }

    request = urllib.request.Request(
        url=f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)

    return result["result"]


def answer_from_knowledge(question: str) -> dict:
    results = search_knowledge(question)

    if not results:
        return {
            "answer": "Nie znalazłem informacji w dostępnej dokumentacji.",
            "sources": []
        }

    context_parts = []
    sources = []

    for item in results:
        payload = item["payload"]

        context_parts.append(payload["text"])
        sources.append(payload["source"])

    context = "\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś AI Production Copilot. "
                "Odpowiadaj po polsku wyłącznie na podstawie "
                "dostarczonej dokumentacji. "
                "Jeśli dokumentacja nie zawiera odpowiedzi, "
                "powiedz, że nie znalazłeś informacji. "
                "Nie wymyślaj procedur produkcyjnych."
            )
        },
        {
            "role": "user",
            "content": (
                f"Pytanie: {question}\n\n"
                f"Dokumentacja:\n{context}"
            )
        }
    ]

    response = chat_completion(messages)

    return {
        "answer": response.get("content", ""),
        "sources": list(dict.fromkeys(sources))
    }