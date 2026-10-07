# Global config values shared across modules

SERVICE_NAME = "python-sentiment-service"
DEFAULT_CONFIDENCE = 0.5
POSITIVE_KEYWORDS = ["good", "love", "amazing", "great", "happy"]
NEGATIVE_KEYWORDS = ["bad", "hate", "terrible", "sad", "angry"]

import os

LEXICON_DB_PATH = os.environ.get("LEXICON_DB_PATH", "lexicon.db")
LEXICON_CONTROLLER_URI = os.environ.get("LEXICON_CONTROLLER_URI", "")
LEXICON_CONTROLLER_USER = os.environ.get("LEXICON_CONTROLLER_USER", "")
LEXICON_CONTROLLER_PASSWORD = os.environ.get("LEXICON_CONTROLLER_PASSWORD", "")
LEXICON_SOURCES = {
    "core": {"container": "core-lexicon", "language": "en"},
    "social": {"container": "social-lexicon", "language": "en"},
}

CACHE_EXPORT_PATH = os.environ.get("CACHE_EXPORT_PATH", "cache_export.jsonl")

WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH", "/sentiment")
WEBHOOK_TIMEOUT_SECONDS = 5
