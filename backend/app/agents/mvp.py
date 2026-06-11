from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import MvpOutput
from app.llm.prompts import MVP_SYSTEM, MVP_USER


async def mvp_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    gap = state.get("gap") or {}
    personas = state.get("personas") or {}

    uvp = gap.get("unique_value_proposition", "No UVP defined yet — derive from the idea.")
    primary_persona = personas.get("primary_persona", "Target user")

    result = await run_agent(
        run_id=run_id,
        agent_name="mvp",
        system=MVP_SYSTEM,
        user=MVP_USER.format(
            idea=idea,
            uvp=uvp,
            primary_persona=primary_persona,
        ),
        schema=MvpOutput,
    )

    if result:
        return {"mvp": result.model_dump(), "raw_sources": [], "errors": []}
    return {"mvp": None, "errors": ["mvp failed"]}
