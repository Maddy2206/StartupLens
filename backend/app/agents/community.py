import asyncio
from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import CommunityOutput
from app.llm.prompts import COMMUNITY_SYSTEM, COMMUNITY_USER
from app.tools.reddit import reddit_search, hn_search, format_community_results


async def community_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    reddit_result, hn_result = await asyncio.gather(
        reddit_search(f"{idea} problems complaints alternatives"),
        hn_search(idea),
    )

    community_data = format_community_results(reddit_result, hn_result)

    sources: list[str] = []
    if reddit_result.success:
        sources += [p.get("url", "") for p in (reddit_result.data or []) if p.get("url")]
    if hn_result.success:
        sources += [h.get("url", "") for h in (hn_result.data or []) if h.get("url")]

    result = await run_agent(
        run_id=run_id,
        agent_name="community",
        system=COMMUNITY_SYSTEM,
        user=COMMUNITY_USER.format(idea=idea, community_data=community_data),
        schema=CommunityOutput,
    )

    if result:
        return {"community": result.model_dump(), "raw_sources": sources, "errors": []}
    return {"community": None, "errors": ["community failed"]}
