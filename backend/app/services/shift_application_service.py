
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_shift import JobShift
from app.models.shift_application import ShiftApplication
from app.models.worker_profile import WorkerProfile
from app.models.worker_skill import WorkerSkill
from app.services.shift_conflicts import has_shift_conflict
from app.services.worker_availability import is_worker_available

async def apply_for_shift(
    db: AsyncSession,
    user_id: uuid.UUID,
    shift_id: uuid.UUID,
) -> ShiftApplication:
    result = await db.execute(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user_id
        )
    )
    worker = result.scalar_one_or_none()

    if worker is None:
        raise ValueError("Worker profile not found")

    # Lock the shift to serialize applications and approvals.
    result = await db.execute(
        select(JobShift)
        .where(JobShift.id == shift_id)
        .with_for_update()
    )
    shift = result.scalar_one_or_none()

    if shift is None or shift.status != "open":
        raise ValueError("Shift is not open")

    if shift.starts_at <= datetime.now(timezone.utc):
        raise ValueError("Shift has already started")

    result = await db.execute(
        select(WorkerSkill.skill_id).where(
            WorkerSkill.worker_profile_id == worker.id,
            WorkerSkill.skill_id == shift.skill_id,
        )
    )

    if result.scalar_one_or_none() is None:
        raise ValueError("Worker does not have the required skill")

    result = await db.execute(
        select(ShiftApplication.id).where(
            ShiftApplication.job_shift_id == shift.id,
            ShiftApplication.worker_profile_id == worker.id,
            ShiftApplication.deleted_at.is_(None),
        )
    )

    if result.scalar_one_or_none() is not None:
        raise ValueError("Worker has already applied")

    result = await db.execute(
        select(func.count(ShiftApplication.id)).where(
            ShiftApplication.job_shift_id == shift.id,
            ShiftApplication.status == "accepted",
            ShiftApplication.deleted_at.is_(None),
        )
    )

    if result.scalar_one() >= shift.workers_needed:
        raise ValueError("Shift is fully staffed")

    if not await is_worker_available(
        db, worker.id, shift.starts_at, shift.ends_at
    ):
        raise ValueError("Worker is not available")

    if await has_shift_conflict(
        db, worker.id, shift.starts_at, shift.ends_at
    ):
        raise ValueError("Worker already has an overlapping shift")

    application = ShiftApplication(
        job_shift_id=shift.id,
        worker_profile_id=worker.id,
        status="pending",
    )

    db.add(application)
    await db.flush()

    return application

async def withdraw_shift_application(
    db: AsyncSession,
    user_id: uuid.UUID,
    application_id: uuid.UUID,
) -> ShiftApplication:
    result = await db.execute(
        select(ShiftApplication)
        .join(
            WorkerProfile,
            ShiftApplication.worker_profile_id == WorkerProfile.id,
        )
        .where(
            ShiftApplication.id == application_id,
            WorkerProfile.user_id == user_id,
            ShiftApplication.deleted_at.is_(None),
        )
        .with_for_update(of=ShiftApplication)
    )

    application = result.scalar_one_or_none()

    if application is None:
        raise ValueError("Application not found")

    if application.status != "pending":
        raise ValueError("Only pending applications can be withdrawn")

    application.status = "withdrawn"
    application.deleted_at = datetime.now(timezone.utc)

    await db.flush()

    return application