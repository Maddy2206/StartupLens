import json
from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import MarketResearchOutput
from app.llm.prompts import MARKET_RESEARCH_SYSTEM, MARKET_RESEARCH_USER
from app.tools.tavily import tavily_search, format_tavily_results


async def market_research_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    search_result = await tavily_search(f"{idea} market size TAM industry trends statistics")
    context = format_tavily_results(search_result.data or []) if search_result.success else "No live search data available — use domain knowledge and clearly label estimates."

    sources = [r.get("url", "") for r in (search_result.data or []) if r.get("url")]

    result = await run_agent(
        run_id=run_id,
        agent_name="market_research",
        system=MARKET_RESEARCH_SYSTEM,
        user=MARKET_RESEARCH_USER.format(idea=idea, context=context),
        schema=MarketResearchOutput,
    )

    if result:
        return {"market_research": result.model_dump(), "raw_sources": sources, "errors": []}
    return {"market_research": None, "errors": ["market_research failed"]}
