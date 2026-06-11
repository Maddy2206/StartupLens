import hashlib
import logging
import httpx
from app.config import get_settings
from app.tools.base import ToolResult, has_key, _cache_get, _cache_set

logger = logging.getLogger(__name__)


async def firecrawl_scrape(url: str) -> ToolResult:
    settings = get_settings()
    if not has_key(settings.firecrawl_api_key):
        return ToolResult(success=False, error="FIRECRAWL_API_KEY not configured")

    cache_key = hashlib.md5(f"firecrawl:{url}".encode()).hexdigest()
    cached = _cache_get(cache_key)
    if cached is not None:
        return ToolResult(success=True, data=cached)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {settings.firecrawl_api_key}"},
                json={"url": url, "formats": ["markdown"]},
            )
            resp.raise_for_status()
            data = resp.json()
            content = data.get("data", {}).get("markdown", "") or data.get("markdown", "")
            _cache_set(cache_key, content)
            return ToolResult(success=True, data=content)
    except Exception as e:
        logger.warning("Firecrawl scrape failed for url '%s': %s", url, e)
        return ToolResult(success=False, error=str(e))
