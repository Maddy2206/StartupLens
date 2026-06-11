import asyncio
import logging
from app.db.session import AsyncSessionLocal
from app.db import crud
from app.db.models import RunStatus
from app.graph.workflow import get_graph
from app.services.events import register_run, push_event, close_run

logger = logging.getLogger(__name__)


async def run_validation(project_id: str, idea: str) -> None:
    """Execute the full validation pipeline as a background task."""
    register_run(project_id)

    async with AsyncSessionLocal() as db:
        await crud.update_project_status(db, project_id, RunStatus.running)

    try:
        graph = get_graph()
        initial_state = {
            "idea": idea,
            "run_id": project_id,
            "raw_sources": [],
            "errors": [],
        }

        final_state = await graph.ainvoke(initial_state)

        # Persist agent outputs from final state
        async with AsyncSessionLocal() as db:
            agent_keys = [
                "plan", "market_research", "competitors", "community",
                "gap", "personas", "business_model", "mvp", "risks",
            ]
            for key in agent_keys:
                data = final_state.get(key)
                await crud.upsert_agent_output(
                    db, project_id, key,
                    status="completed" if data else "failed",
                    output=data,
                )

            # Save final report
            report_data = final_state.get("report")
            if report_data:
                await crud.save_report(
                    db,
                    project_id,
                    data=report_data,
                    validation_score=report_data.get("validation_score"),
                    differentiation_score=report_data.get("differentiation_score"),
                )
                await crud.update_project_status(db, project_id, RunStatus.completed)
            else:
                await crud.update_project_status(db, project_id, RunStatus.failed)

        await push_event(project_id, {
            "event": "run_completed",
            "run_id": project_id,
            "data": final_state.get("report"),
        })

    except Exception as e:
        logger.error("run_validation failed for %s: %s", project_id, e, exc_info=True)
        async with AsyncSessionLocal() as db:
            await crud.update_project_status(db, project_id, RunStatus.failed)
        await push_event(project_id, {
            "event": "error",
            "run_id": project_id,
            "error": str(e),
        })
    finally:
        await close_run(project_id)


def spawn_validation(project_id: str, idea: str) -> None:
    """Fire-and-forget: create an asyncio task for the validation pipeline."""
    asyncio.create_task(run_validation(project_id, idea))
