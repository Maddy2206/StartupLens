import json
from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import GapOutput
from app.llm.prompts import GAP_SYSTEM, GAP_USER


def _summarize_competitors(competitors: dict | None) -> str:
    if not competitors:
        return "No competitor data available."
    direct = competitors.get("direct_competitors", [])
    lines = []
    for c in direct[:5]:
        lines.append(f"- {c.get('name')}: weakness = {c.get('weakness', 'unknown')}")
    return "\n".join(lines) if lines else competitors.get("summary", "")


def _summarize_community(community: dict | None) -> str:
    if not community:
        return "No community data available."
    pain_points = community.get("pain_points", [])
    lines = [f"- [{p.get('frequency', '?')} freq] {p.get('pain_point', '')}" for p in pain_points[:8]]
    return "\n".join(lines) if lines else community.get("summary", "")


async def gap_opportunity_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    competitor_summary = _summarize_competitors(state.get("competitors"))
    community_summary = _summarize_community(state.get("community"))

    result = await run_agent(
        run_id=run_id,
        agent_name="gap_opportunity",
        system=GAP_SYSTEM,
        user=GAP_USER.format(
            idea=idea,
            competitor_summary=competitor_summary,
            community_summary=community_summary,
        ),
        schema=GapOutput,
    )

    if result:
        return {"gap": result.model_dump(), "raw_sources": [], "errors": []}
    return {"gap": None, "errors": ["gap_opportunity failed"]}
