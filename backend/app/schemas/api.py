from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
from app.db.models import RunStatus


class ValidateRequest(BaseModel):
    idea: str


class ProjectResponse(BaseModel):
    id: str
    idea: str
    status: RunStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]


class SSEEvent(BaseModel):
    event: str
    run_id: str
    agent: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None
