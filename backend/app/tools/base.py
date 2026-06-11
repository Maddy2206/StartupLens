import time
import logging
from typing import Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


# Simple in-memory TTL cache — avoids duplicate tool calls within a pipeline run
_cache: dict[str, tuple[float, Any]] = {}
_TTL = 300  # 5 minutes


def _cache_get(key: str) -> Optional[Any]:
    entry = _cache.get(key)
    if entry and time.time() - entry[0] < _TTL:
        return entry[1]
    return None


def _cache_set(key: str, value: Any) -> None:
    _cache[key] = (time.time(), value)


def has_key(value: str) -> bool:
    return bool(value and value.strip())
