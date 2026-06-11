import asyncio
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db import crud
from app.schemas.api import ValidateRequest, ProjectResponse, ProjectListResponse
from app.services.runner import spawn_validation
from app.services.events import get_queue

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/validate", response_model=ProjectResponse, status_code=201)
async def create_validation(body: ValidateRequest, db: AsyncSession = Depends(get_db)):
    if not body.idea or len(body.idea.strip()) < 10:
        raise HTTPException(400, "Idea must be at least 10 characters.")
    project = await crud.create_project(db, body.idea.strip())
    spawn_validation(project.id, project.idea)
    return project


@router.get("/validate", response_model=ProjectListResponse)
async def list_validations(db: AsyncSession = Depends(get_db)):
    projects = await crud.list_projects(db)
    return {"projects": projects}


@router.get("/validate/{project_id}", response_model=dict)
async def get_validation(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await crud.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found.")

    report = await crud.get_report(db, project_id)
    return {
        "project": ProjectResponse.model_validate(project).model_dump(),
        "report": report.data if report else None,
    }


@router.get("/validate/{project_id}/stream")
async def stream_validation(project_id: str):
    async def event_generator():
        # Wait briefly for the queue to be registered (race between POST and SSE open)
        for _ in range(20):
            q = get_queue(project_id)
            if q is not None:
                break
            await asyncio.sleep(0.2)

        q = get_queue(project_id)
        if q is None:
            # Run may already be done — send a synthetic done event
            yield f"data: {json.dumps({'event': 'run_not_found', 'run_id': project_id})}\n\n"
            return

        while True:
            try:
                event = await asyncio.wait_for(q.get(), timeout=120)
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'event': 'keepalive', 'run_id': project_id})}\n\n"
                continue

            if event is None:  # sentinel — stream closed
                break

            yield f"data: {json.dumps(event)}\n\n"

            if event.get("event") in ("run_completed", "error"):
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")
