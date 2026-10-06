from config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS
from core.confidence_utils import compute_confidence
from core.normalizer import clean_text

def score_text(text: str) -> tuple[int, int]:
    """Return (score, matched keyword count) for the text."""
    normalized = clean_text(text)
    score = 0
    matched = 0
    for word in POSITIVE_KEYWORDS:
        if word in normalized:
            score += 1
            matched += 1
    for word in NEGATIVE_KEYWORDS:
        if word in normalized:
            score -= 1
            matched += 1
    return score, matched


def determine_sentiment(score: int) -> str:
    """Map a keyword score to a sentiment label."""
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"


def analyze_sentiment_pipeline(text: str) -> dict:
    """Complete multi-step sentiment analysis pipeline."""
    score, matched = score_text(text)
    sentiment = determine_sentiment(score)
    confidence = compute_confidence(sentiment, score, matched)
    return {
        "sentiment": sentiment,
        "confidence": confidence
    }
