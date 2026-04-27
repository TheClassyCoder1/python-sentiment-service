def clean_text(text: str) -> str:
    """Normalize user input text before sentiment analysis."""
    if not text:
        return ""
    return text.strip().lower()
