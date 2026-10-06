from fastapi import FastAPI, HTTPException
from models.request_response import TextRequest, SentimentResult
from core.sentiment_engine import analyze_sentiment_pipeline
from repository.cache_repository import get_from_cache, save_to_cache
from core.http_client import fetch_external_quote
from config import SERVICE_NAME
from api import documents, lexicon
import asyncio

app = FastAPI(title=SERVICE_NAME)
app.include_router(documents.router)
app.include_router(lexicon.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=SentimentResult)
async def analyze(req: TextRequest):
    """Perform cached multi-step sentiment analysis with external API enrichment."""
    try:
        cached = get_from_cache(req.text)
        if cached:
            return SentimentResult(**cached)

        # Step 1: sentiment analysis
        result = analyze_sentiment_pipeline(req.text)
        result["source"] = SERVICE_NAME

        # Step 2: fetch a quote asynchronously
        quote = await fetch_external_quote()
        if quote and "Quote service" not in quote:
            # add quote snippet if available
            result["quote_snippet"] = quote[:50] + "..." if len(quote) > 50 else quote
        else:
            result["quote_snippet"] = "No quote available"

        # Step 3: cache result
        save_to_cache(req.text, result)
        return SentimentResult(**result)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
