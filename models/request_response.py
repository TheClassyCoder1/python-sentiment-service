from typing import Literal

from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    text: str

class SentimentResult(BaseModel):
    sentiment: str
    confidence: float
    source: str
    quote_snippet: str | None = None


class DocumentCreate(BaseModel):
    text: str
    language: str | None = None


class DocumentRead(BaseModel):
    id: int
    owner_id: str
    text: str
    sentiment: str
    confidence: float


class QualityCheckRequest(BaseModel):
    column: Literal["term", "weight", "source"]
    checks: list[Literal["null_check", "distinct_check", "min", "max"]] = Field(min_length=1)
