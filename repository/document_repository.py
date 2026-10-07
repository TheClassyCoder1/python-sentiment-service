import itertools

_DOCUMENTS: dict[int, dict] = {}
_IDS = itertools.count(1)


def create(*, owner_id: str, text: str, sentiment: str, confidence: float) -> dict:
    document = {
        "id": next(_IDS),
        "owner_id": owner_id,
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
    }
    _DOCUMENTS[document["id"]] = document
    return document


def get(*, document_id: int) -> dict | None:
    return _DOCUMENTS.get(document_id)


def delete(*, document_id: int) -> None:
    """Deletes an existing document."""
    document = _DOCUMENTS.get(document_id)
    del _DOCUMENTS[document["id"]]
