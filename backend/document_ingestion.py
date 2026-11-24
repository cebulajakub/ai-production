import hashlib
from pathlib import Path

from rag_service import get_embedding


DOCUMENTS_DIR = Path("/app/documents")


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Split text into chunks, preserving words where possible."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        candidate = " ".join(current_chunk + [word])

        if len(candidate) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def create_point_id(source: str, chunk_index: int) -> str:
    """Create a deterministic UUID from document and chunk index."""
    import uuid

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"manufacturing_knowledge:{source}:{chunk_index}"
        )
    )


def prepare_document(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    points = []

    for index, chunk in enumerate(chunks):
        points.append({
            "id": create_point_id(path.name, index),
            "vector": get_embedding(
                chunk,
                task="search_document"
            ),
            "payload": {
                "text": chunk,
                "source": path.name,
                "chunk_index": index,
                "content_hash": hashlib.sha256(
                    chunk.encode("utf-8")
                ).hexdigest()
            }
        })

    return points