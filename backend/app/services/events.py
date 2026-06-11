"""In-process asyncio.Queue registry for SSE streaming. One queue per active run."""
import asyncio
from typing import Any

_queues: dict[str, asyncio.Queue] = {}
_SENTINEL = None  # pushed to signal stream end


def register_run(run_id: str) -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue()
    _queues[run_id] = q
    return q


def get_queue(run_id: str) -> asyncio.Queue | None:
    return _queues.get(run_id)


async def push_event(run_id: str, event: dict) -> None:
    q = _queues.get(run_id)
    if q is not None:
        await q.put(event)


async def close_run(run_id: str) -> None:
    q = _queues.get(run_id)
    if q is not None:
        await q.put(_SENTINEL)
        _queues.pop(run_id, None)
