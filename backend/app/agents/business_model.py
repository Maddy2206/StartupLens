from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import BusinessModelOutput
from app.llm.prompts import BUSINESS_MODEL_SYSTEM, BUSINESS_MODEL_USER


def _personas_summary(personas: dict | None) -> str:
    if not personas:
        return "No persona data."
    ps = personas.get("personas", [])
    return "\n".join(f"- {p.get('role')} ({p.get('age_range')}): WTP = {p.get('willingness_to_pay')}" for p in ps[:3])


def _competitor_pricing(competitors: dict | None) -> str:
    if not competitors:
        return "No competitor pricing data."
    direct = competitors.get("direct_competitors", [])
    return "\n".join(f"- {c.get('name')}: {c.get('pricing', 'unknown')}" for c in direct[:5])


async def business_model_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]
    market = state.get("market_research") or {}

    result = await run_agent(
        run_id=run_id,
        agent_name="business_model",
        system=BUSINESS_MODEL_SYSTEM,
        user=BUSINESS_MODEL_USER.format(
            idea=idea,
            personas_summary=_personas_summary(state.get("personas")),
            competitor_pricing=_competitor_pricing(state.get("competitors")),
            market_summary=market.get("summary", idea),
        ),
        schema=BusinessModelOutput,
    )

    if result:
        return {"business_model": result.model_dump(), "raw_sources": [], "errors": []}
    return {"business_model": None, "errors": ["business_model failed"]}
