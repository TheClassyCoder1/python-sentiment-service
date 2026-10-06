from config import DEFAULT_CONFIDENCE

def compute_confidence(sentiment: str, score: int, matched: int) -> float:
    """Compute confidence from how strongly the matched keywords agree."""
    if sentiment == "neutral" and matched == 0:
        return DEFAULT_CONFIDENCE
    return round(abs(score) / matched, 2)
