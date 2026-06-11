from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import PersonaOutput
from app.llm.prompts import PERSONA_SYSTEM, PERSONA_USER


async def persona_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    gap = state.get("gap") or {}
    community = state.get("community") or {}

    gaps = "\n".join(gap.get("market_gaps", [])) or "Analyze from the idea itself."
    community_summary = community.get("summary", "No community data available.")

    result = await run_agent(
        run_id=run_id,
        agent_name="persona",
        system=PERSONA_SYSTEM,
        user=PERSONA_USER.format(
            idea=idea,
            gaps=gaps,
            community_summary=community_summary,
        ),
        schema=PersonaOutput,
    )

    if result:
        return {"personas": result.model_dump(), "raw_sources": [], "errors": []}
    return {"personas": None, "errors": ["persona failed"]}
