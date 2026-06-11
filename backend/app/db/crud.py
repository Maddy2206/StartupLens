from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Project, AgentOutput, Report, RunStatus


async def create_project(db: AsyncSession, idea: str) -> Project:
    project = Project(idea=idea, status=RunStatus.pending)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_project(db: AsyncSession, project_id: str) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def list_projects(db: AsyncSession, limit: int = 20) -> list[Project]:
    result = await db.execute(select(Project).order_by(Project.created_at.desc()).limit(limit))
    return list(result.scalars().all())


async def update_project_status(db: AsyncSession, project_id: str, status: RunStatus) -> None:
    project = await get_project(db, project_id)
    if project:
        project.status = status
        await db.commit()


async def upsert_agent_output(
    db: AsyncSession,
    project_id: str,
    agent_name: str,
    status: str,
    output: dict | None = None,
    error: str | None = None,
) -> AgentOutput:
    result = await db.execute(
        select(AgentOutput).where(
            AgentOutput.project_id == project_id,
            AgentOutput.agent_name == agent_name,
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        row = AgentOutput(project_id=project_id, agent_name=agent_name)
        db.add(row)

    row.status = status
    if output is not None:
        row.output = output
    if error is not None:
        row.error = error
    if status in ("completed", "failed"):
        row.completed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(row)
    return row


async def save_report(
    db: AsyncSession,
    project_id: str,
    data: dict,
    validation_score: int | None,
    differentiation_score: int | None,
) -> Report:
    result = await db.execute(select(Report).where(Report.project_id == project_id))
    report = result.scalar_one_or_none()
    if report is None:
        report = Report(project_id=project_id)
        db.add(report)

    report.data = data
    report.validation_score = validation_score
    report.differentiation_score = differentiation_score
    await db.commit()
    await db.refresh(report)
    return report


async def get_report(db: AsyncSession, project_id: str) -> Report | None:
    result = await db.execute(select(Report).where(Report.project_id == project_id))
    return result.scalar_one_or_none()
