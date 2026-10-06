import asyncio
import hashlib
import hmac
import json
import os
from collections import OrderedDict
from dataclasses import dataclass

from fastapi import Header, HTTPException, status


@dataclass(frozen=True)
class AuthIdentity:
    user_id: str


class _IdentityCache:
    def __init__(self, max_entries: int = 1024):
        self._items: OrderedDict[str, AuthIdentity | None] = OrderedDict()
        self._max_entries = max_entries

    def get(self, key: str) -> AuthIdentity | None:
        return self._items.get(key)

    def set(self, key: str, value: AuthIdentity | None) -> None:
        self._items[key] = value
        self._items.move_to_end(key)
        while len(self._items) > self._max_entries:
            self._items.popitem(last=False)


class TokenValidator:
    def __init__(self, tokens: dict[str, str]):
        self._tokens = tokens
        self._cache = _IdentityCache()
        self._lock = asyncio.Lock()

    async def _validate(self, credential: str) -> AuthIdentity | None:
        for token, user_id in self._tokens.items():
            if hmac.compare_digest(token.encode("utf-8"), credential.encode("utf-8")):
                return AuthIdentity(user_id=user_id)
        return None

    async def _validate_and_cache(
        self,
        cache_key: str,
        credential: str,
    ) -> AuthIdentity | None:
        identity = await self._validate(credential)
        async with self._lock:
            self._cache.set(cache_key, identity)
        return identity

    async def authenticate(self, credential: str) -> AuthIdentity | None:
        cache_key = hashlib.sha256(credential.encode("utf-8")).hexdigest()
        async with self._lock:
            identity = self._cache.get(cache_key)
        if identity is not None:
            return identity
        return await self._validate_and_cache(cache_key, credential)


_validator = TokenValidator(json.loads(os.environ.get("API_TOKENS", "{}")))


async def get_current_user(authorization: str | None = Header(default=None)) -> AuthIdentity:
    scheme, _, credential = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not credential:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    identity = await _validator.authenticate(credential)
    if identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return identity
