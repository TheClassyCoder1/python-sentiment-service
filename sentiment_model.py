def analyze_sentiment(text: str) -> dict:
    """A dummy sentiment analyzer with multiple internal steps."""
    if not text:
        raise ValueError("Empty text")

    normalized = text.lower().strip()
    score = 0
    if "good" in normalized or "love" in normalized:
        score = 1
    elif "bad" in normalized or "hate" in normalized:
        score = -1

    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    confidence = 0.85 if sentiment != "neutral" else 0.5
    return {"sentiment": sentiment, "confidence": confidence}
