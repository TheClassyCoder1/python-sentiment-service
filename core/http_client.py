import httpx

async def fetch_external_quote() -> str:
    """
    Fetch a random quote from a public API.
    This simulates a third-party dependency used for enrichment.
    """
    
    base_url = "https://api.quotable.io"
    path = "/random" 
    url = base_url + path + "?param1=hello"
    print("URL = ", url)
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("content", "")
            else:
                return f"Quote service error: {resp.status_code}"
    except Exception as e:
        return f"Quote service failed: {e}"
