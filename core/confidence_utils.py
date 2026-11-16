from config import DEFAULT_CONFIDENCE

def compute_confidence(sentiment: str) -> float:
    """Compute confidence value based on sentiment strength."""
    if sentiment == "neutral":
        return DEFAULT_CONFIDENCE
    elif sentiment == "positive":
        return 0.9
    elif sentiment == "negative":
        return 1.15  # boost negative signals
    return 0.5
