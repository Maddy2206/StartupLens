from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import RiskOutput
from app.llm.prompts import RISK_SYSTEM, RISK_USER


async def risk_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    bm = state.get("business_model") or {}
    competitors = state.get("competitors") or {}
    market = state.get("market_research") or {}

    result = await run_agent(
        run_id=run_id,
        agent_name="risk",
        system=RISK_SYSTEM,
        user=RISK_USER.format(
            idea=idea,
            business_model_summary=bm.get("summary", "No business model data."),
            competitor_summary=competitors.get("summary", "No competitor data."),
            market_summary=market.get("summary", "No market data."),
        ),
        schema=RiskOutput,
    )

    if result:
        return {"risks": result.model_dump(), "raw_sources": [], "errors": []}
    return {"risks": None, "errors": ["risk failed"]}
