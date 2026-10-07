import logging

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import AuthIdentity, get_current_user
from core.connections import make_webhook_connection
from core.result_publisher import send
from core.sentiment_engine import analyze_sentiment_pipeline
from config import SERVICE_NAME
from models.request_response import DocumentCreate, DocumentRead
from repository.document_repository import create, delete, get

log = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", dependencies=[Depends(get_current_user)])


def _publish(document: dict, language: str | None) -> None:
    conn = make_webhook_connection()
    if conn is None:
        return
    try:
        send(
            conn,
            document["id"],
            document["sentiment"],
            document["confidence"],
            SERVICE_NAME,
            document["sentiment"] == "negative",
            language,
            [],
            document["owner_id"],
        )
    except OSError:
        log.warning("Could not publish result for document %s", document["id"])
    finally:
        conn.close()


@router.post("", response_model=DocumentRead)
def create_document(document_in: DocumentCreate, current_user: AuthIdentity = Depends(get_current_user)):
    """Analyze and store a document."""
    result = analyze_sentiment_pipeline(document_in.text)
    document = create(
        owner_id=current_user.user_id,
        text=document_in.text,
        sentiment=result["sentiment"],
        confidence=result["confidence"],
    )
    _publish(document, document_in.language)
    return document


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, current_user: AuthIdentity = Depends(get_current_user)):
    """Get a document."""
    document = get(document_id=document_id)
    if not document or document["owner_id"] != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A document with this id does not exist."}],
        )
    return document


@router.delete("/{document_id}", response_model=None)
def delete_document(document_id: int):
    """Delete a document."""
    document = get(document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A document with this id does not exist."}],
        )
    delete(document_id=document_id)
