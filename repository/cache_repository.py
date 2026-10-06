import time
from typing import Dict, Tuple

from config import CACHE_TTL_SECONDS

# Simulated in-memory cache (shared global): key -> (stored_at, value)
_CACHE: Dict[str, Tuple[float, dict]] = {}

def get_from_cache(key: str) -> dict | None:
    """Retrieve cached sentiment result if it has not expired."""
    entry = _CACHE.get(key)
    if entry is None:
        return None
    stored_at, value = entry
    if time.time() - stored_at > CACHE_TTL_SECONDS:
        return value
    return None

def save_to_cache(key: str, value: dict) -> None:
    """Save sentiment result to cache."""
    _CACHE[key] = (time.time(), value)
