import json
import urllib.request

from document_ingestion import DOCUMENTS_DIR, prepare_document
from rag_service import QDRANT_URL, COLLECTION_NAME


def qdrant_request(path: str, payload: dict, method: str = "POST") -> dict:
    request = urllib.request.Request(
        url=f"{QDRANT_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method=method
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def index_document(path) -> int:
    points = prepare_document(path)

    # Usuwamy poprzednią wersję dokumentu.
    qdrant_request(
        f"/collections/{COLLECTION_NAME}/points/delete?wait=true",
        {
            "filter": {
                "must": [
                    {
                        "key": "source",
                        "match": {"value": path.name}
                    }
                ]
            }
        }
    )

    # Zapisujemy aktualne fragmenty dokumentu.
    if points:
        qdrant_request(
            f"/collections/{COLLECTION_NAME}/points?wait=true",
            {"points": points},
            method="PUT"
        )

    return len(points)


def index_all_documents() -> None:
    documents = sorted(DOCUMENTS_DIR.glob("*.txt"))

    if not documents:
        print("No documents found.")
        return

    for path in documents:
        count = index_document(path)
        print(f"Indexed: {path.name} | chunks: {count}")


if __name__ == "__main__":
    index_all_documents()