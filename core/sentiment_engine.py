from config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS
from core.confidence_utils import compute_confidence
from core.normalizer import clean_text

def determine_sentiment(text: str) -> str:
    """Core sentiment determination logic."""
    normalized = clean_text(text)
    if not normalized:
        return "neutral"
    
    score = 0
    for word in POSITIVE_KEYWORDS:
        if word in normalized:
            score += 1
    for word in NEGATIVE_KEYWORDS:
        if word in normalized:
            score -= 1

    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


def analyze_sentiment_pipeline(text: str) -> dict:
    """Complete multi-step sentiment analysis pipeline."""
    sentiment = determine_sentiment(text)
    confidence = compute_confidence(sentiment)
    return {
        "sentiment": sentiment,
        "confidence": confidence
    }

