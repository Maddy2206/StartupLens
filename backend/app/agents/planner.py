from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import PlanOutput
from app.llm.prompts import PLANNER_SYSTEM, PLANNER_USER


async def planner_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    result = await run_agent(
        run_id=run_id,
        agent_name="planner",
        system=PLANNER_SYSTEM,
        user=PLANNER_USER.format(idea=idea),
        schema=PlanOutput,
    )

    if result:
        return {"plan": result.model_dump(), "raw_sources": [], "errors": []}
    return {"plan": None, "errors": ["planner failed"]}
