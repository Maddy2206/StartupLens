from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import CompetitorOutput
from app.llm.prompts import COMPETITOR_SYSTEM, COMPETITOR_USER
from app.tools.tavily import tavily_search, format_tavily_results


async def competitor_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]
    market = state.get("market_research") or {}
    market_context = market.get("summary", idea)

    search_result = await tavily_search(f"{idea} competitors alternatives comparison pricing features")
    search_text = format_tavily_results(search_result.data or []) if search_result.success else "No live search data — reason from knowledge."

    sources = [r.get("url", "") for r in (search_result.data or []) if r.get("url")]

    result = await run_agent(
        run_id=run_id,
        agent_name="competitor",
        system=COMPETITOR_SYSTEM,
        user=COMPETITOR_USER.format(
            idea=idea,
            market_context=market_context,
            search_results=search_text,
        ),
        schema=CompetitorOutput,
    )

    if result:
        return {"competitors": result.model_dump(), "raw_sources": sources, "errors": []}
    return {"competitors": None, "errors": ["competitor failed"]}
