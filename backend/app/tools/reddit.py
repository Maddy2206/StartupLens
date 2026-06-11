import hashlib
import logging
import httpx
from app.config import get_settings
from app.tools.base import ToolResult, has_key, _cache_get, _cache_set

logger = logging.getLogger(__name__)


async def reddit_search(query: str, limit: int = 10) -> ToolResult:
    """Search Reddit via the public JSON search endpoint (no auth required for basic search)."""
    settings = get_settings()
    cache_key = hashlib.md5(f"reddit:{query}:{limit}".encode()).hexdigest()
    cached = _cache_get(cache_key)
    if cached is not None:
        return ToolResult(success=True, data=cached)

    try:
        headers = {"User-Agent": settings.reddit_user_agent}
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://www.reddit.com/search.json",
                params={"q": query, "limit": limit, "sort": "relevance", "t": "year"},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            posts = []
            for child in data.get("data", {}).get("children", []):
                p = child.get("data", {})
                posts.append({
                    "title": p.get("title", ""),
                    "subreddit": p.get("subreddit", ""),
                    "score": p.get("score", 0),
                    "selftext": (p.get("selftext") or "")[:500],
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "num_comments": p.get("num_comments", 0),
                })
            _cache_set(cache_key, posts)
            return ToolResult(success=True, data=posts)
    except Exception as e:
        logger.warning("Reddit search failed for query '%s': %s", query, e)
        return ToolResult(success=False, error=str(e))


async def hn_search(query: str, limit: int = 10) -> ToolResult:
    """Search Hacker News via Algolia API (no auth required)."""
    cache_key = hashlib.md5(f"hn:{query}:{limit}".encode()).hexdigest()
    cached = _cache_get(cache_key)
    if cached is not None:
        return ToolResult(success=True, data=cached)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://hn.algolia.com/api/v1/search",
                params={"query": query, "hitsPerPage": limit, "tags": "story"},
            )
            resp.raise_for_status()
            data = resp.json()
            hits = []
            for h in data.get("hits", []):
                hits.append({
                    "title": h.get("title", ""),
                    "url": h.get("url", ""),
                    "points": h.get("points", 0),
                    "num_comments": h.get("num_comments", 0),
                    "story_text": (h.get("story_text") or "")[:400],
                })
            _cache_set(cache_key, hits)
            return ToolResult(success=True, data=hits)
    except Exception as e:
        logger.warning("HN search failed for query '%s': %s", query, e)
        return ToolResult(success=False, error=str(e))


def format_community_results(reddit_result: ToolResult, hn_result: ToolResult) -> str:
    parts = []
    if reddit_result.success and reddit_result.data:
        reddit_lines = [f"REDDIT:"]
        for p in reddit_result.data[:5]:
            reddit_lines.append(f"• [{p['subreddit']}] {p['title']} ({p['score']} pts, {p['num_comments']} comments)")
            if p.get("selftext"):
                reddit_lines.append(f"  \"{p['selftext'][:200]}\"")
        parts.append("\n".join(reddit_lines))

    if hn_result.success and hn_result.data:
        hn_lines = ["HACKER NEWS:"]
        for h in hn_result.data[:5]:
            hn_lines.append(f"• {h['title']} ({h.get('points', 0)} pts, {h.get('num_comments', 0)} comments)")
        parts.append("\n".join(hn_lines))

    if not parts:
        return "No live community data available — analyze based on domain knowledge."
    return "\n\n".join(parts)
