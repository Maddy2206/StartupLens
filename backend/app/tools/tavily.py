import hashlib
import logging
import httpx
from app.config import get_settings
from app.tools.base import ToolResult, has_key, _cache_get, _cache_set

logger = logging.getLogger(__name__)


async def tavily_search(query: str, max_results: int = 5) -> ToolResult:
    settings = get_settings()
    if not has_key(settings.tavily_api_key):
        return ToolResult(success=False, error="TAVILY_API_KEY not configured")

    cache_key = hashlib.md5(f"tavily:{query}:{max_results}".encode()).hexdigest()
    cached = _cache_get(cache_key)
    if cached is not None:
        return ToolResult(success=True, data=cached)

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "advanced",
                    "include_answer": True,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            results = [
                {"title": r.get("title"), "url": r.get("url"), "content": r.get("content", "")}
                for r in data.get("results", [])
            ]
            if data.get("answer"):
                results.insert(0, {"title": "Summary", "url": "", "content": data["answer"]})
            _cache_set(cache_key, results)
            return ToolResult(success=True, data=results)
    except Exception as e:
        logger.warning("Tavily search failed for query '%s': %s", query, e)
        return ToolResult(success=False, error=str(e))


def format_tavily_results(results: list[dict]) -> str:
    if not results:
        return "No results."
    lines = []
    for r in results[:5]:
        lines.append(f"[{r.get('title', 'Result')}]\n{r.get('content', '')[:800]}")
    return "\n\n".join(lines)
