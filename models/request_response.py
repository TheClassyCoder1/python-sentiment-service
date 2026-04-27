from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class SentimentResult(BaseModel):
    sentiment: str
    confidence: float
    source: str
    quote_snippet: str | None = None
