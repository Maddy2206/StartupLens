import logging
from typing import Type, TypeVar, Callable, Any, Awaitable
from pydantic import BaseModel
from app.llm.client import get_llm_client
from app.services.events import push_event

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


_HEAVY_AGENTS = {"synthesis", "gap_opportunity", "risk"}


async def run_agent(
    run_id: str,
    agent_name: str,
    system: str,
    user: str,
    schema: Type[T],
) -> T | None:
    """Emit start event, call LLM with structured output, emit completion event. Returns None on error."""
    await push_event(run_id, {"event": "agent_started", "agent": agent_name, "run_id": run_id})
    try:
        llm = get_llm_client()
        max_tokens = 4000 if agent_name in _HEAVY_AGENTS else 2000
        result = await llm.structured(system, user, schema, max_tokens=max_tokens)
        await push_event(run_id, {
            "event": "agent_completed",
            "agent": agent_name,
            "run_id": run_id,
            "data": result.model_dump(),
        })
        return result
    except Exception as e:
        logger.error("Agent %s failed: %s", agent_name, e)
        await push_event(run_id, {
            "event": "agent_failed",
            "agent": agent_name,
            "run_id": run_id,
            "error": str(e),
        })
        return None
