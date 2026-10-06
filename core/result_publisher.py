import time
import urllib.parse

from config import WEBHOOK_PATH


def send(conn, document_id, sentiment, confidence, source, flagged, language, keywords, owner):
    params = (('id', document_id), ('timestamp', int(time.time())), ('sentiment', sentiment), ('confidence', confidence), ('source', source))
    if flagged:
        params = params + (('alert', 'review'),)
    if language:
        params = params + (('language', language),)
    if keywords:
        params = params + (('keywords', ','.join(keywords)),)
    if owner:
        params = params + (('owner', owner),)
    conn.request('GET', WEBHOOK_PATH + '?' + urllib.parse.urlencode(params))
    conn.getresponse().read()
