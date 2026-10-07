import logging
import threading
from contextlib import closing

from fastapi import APIRouter, Depends, HTTPException, Query, status

from config import CACHE_EXPORT_PATH, LEXICON_DB_PATH
from core.auth import get_current_user
from core.lexicon_client import LexiconSourceError, get_controller_client
from core.quality_checks import LEXICON_TABLE, ColumnQualityCheck
from core.usage import UsageTracker
from models.request_response import QualityCheckRequest
from repository.cache_export import CacheExporter
from repository.lexicon_store import LexiconStore

log = logging.getLogger(__name__)

router = APIRouter(prefix="/lexicon", dependencies=[Depends(get_current_user)])

USAGE_LOCK = threading.Lock()
usage_tracker = UsageTracker("lexicon-api")


@router.get("/schemas")
def list_schemas():
    controller = get_controller_client()
    if controller is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lexicon controller is not configured")
    try:
        return {"schemas": controller.get_schemas()}
    except (LexiconSourceError, OSError):
        log.exception("Failed to load lexicon schemas")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Lexicon controller unavailable")


@router.get("/tables")
def list_tables(names: list[str] = Query(default=[])):
    with closing(LexiconStore(LEXICON_DB_PATH)) as store:
        return {"tables": store.get_tables(None, names)}


@router.post("/quality-checks")
def run_quality_checks(req: QualityCheckRequest):
    check = ColumnQualityCheck(LEXICON_TABLE)
    with closing(LexiconStore(LEXICON_DB_PATH)) as store:
        return {"results": check.run(store.connection, req.column, {name: {} for name in req.checks})}


@router.post("/cache/export")
def export_cache():
    saved = CacheExporter.from_cache().save_to_filename(CACHE_EXPORT_PATH)
    return {"saved": saved}


@router.get("/usage")
def usage():
    with USAGE_LOCK:
        return {"usage": usage_tracker.compute_usage_snapshot()}
