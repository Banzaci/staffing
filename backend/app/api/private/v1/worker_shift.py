import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shift_application import ShiftApplication
from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.job_shift import JobShift
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.worker_profile import WorkerProfile

router = APIRouter(prefix="/worker/shifts", tags=["Worker Shifts"])

@router.post("/{shift_id}/apply", status_code=201)
async def apply_for_shift(
    shift_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    worker = await db.scalar(
        select(WorkerProfile).where(WorkerProfile.user_id == user.id)
    )

    if not worker:
        raise HTTPException(403, "Worker profile not found")

    shift = await db.get(JobShift, shift_id)

    if not shift or shift.status != "open":
        raise HTTPException(404, "Open shift not found")

    existing = await db.scalar(
        select(ShiftApplication).where(
            ShiftApplication.job_shift_id == shift_id,
            ShiftApplication.worker_profile_id == worker.id,
            ShiftApplication.deleted_at.is_(None),
        )
    )

    if existing:
        return {"id": existing.id, "status": existing.status}

    application = ShiftApplication(
        job_shift_id=shift_id,
        worker_profile_id=worker.id,
        status="pending",
    )

    db.add(application)
    await db.commit()
    await db.refresh(application)

    return {
        "id": application.id,
        "status": application.status,
    }


@router.get("/applications")
async def get_my_applications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    worker = await db.scalar(
        select(WorkerProfile).where(WorkerProfile.user_id == user.id)
    )

    if not worker:
        return []

    result = await db.execute(
        select(ShiftApplication).where(
            ShiftApplication.worker_profile_id == worker.id,
            ShiftApplication.deleted_at.is_(None),
        )
    )

    return [
        {
            "id": application.id,
            "job_shift_id": application.job_shift_id,
            "status": application.status,
        }
        for application in result.scalars().all()
    ]