import http.client

from config import WEBHOOK_HOST, WEBHOOK_TIMEOUT_SECONDS


def make_webhook_connection() -> http.client.HTTPSConnection | None:
    if not WEBHOOK_HOST:
        return None
    return http.client.HTTPSConnection(WEBHOOK_HOST, timeout=WEBHOOK_TIMEOUT_SECONDS)
