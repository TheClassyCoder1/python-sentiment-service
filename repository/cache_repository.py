from typing import Dict

# Simulated in-memory cache (shared global)
_CACHE: Dict[str, dict] = {}

def get_from_cache(key: str) -> dict | None:
    """Retrieve cached sentiment result if exists."""
    return _CACHE.get(key)

def save_to_cache(key: str, value: dict) -> None:
    """Save sentiment result to cache."""
    _CACHE[key] = value
