
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.business import Business
from app.services.work_authorization import has_work_authorization
from app.models.job_shift import JobShift
from app.models.shift_application import ShiftApplication
from app.models.worker_profile import WorkerProfile
from app.services.shift_conflicts import has_shift_conflict
from app.services.worker_availability import is_worker_available

async def approve_shift_application(
    db: AsyncSession,
    application_id: uuid.UUID,
) -> ShiftApplication:
    result = await db.execute(
        select(ShiftApplication).where(
            ShiftApplication.id == application_id,
            ShiftApplication.deleted_at.is_(None),
        )
    )
    application = result.scalar_one_or_none()

    if application is None:
        raise ValueError("Application not found")

    result = await db.execute(
        select(WorkerProfile.id)
        .where(WorkerProfile.id == application.worker_profile_id)
        .with_for_update()
    )

    if result.scalar_one_or_none() is None:
        raise ValueError("Worker not found")

    result = await db.execute(
        select(JobShift)
        .where(JobShift.id == application.job_shift_id)
        .with_for_update()
    )
    shift = result.scalar_one_or_none()

    if shift is None or shift.status != "open":
        raise ValueError("Shift is not open")

    result = await db.execute(
        select(ShiftApplication)
        .where(
            ShiftApplication.id == application_id,
            ShiftApplication.deleted_at.is_(None),
        )
        .with_for_update()
    )
    application = result.scalar_one_or_none()

    if application is None or application.status != "pending":
        raise ValueError("Application is not pending")

    result = await db.execute(
        select(func.count(ShiftApplication.id)).where(
            ShiftApplication.job_shift_id == shift.id,
            ShiftApplication.status == "accepted",
            ShiftApplication.deleted_at.is_(None),
        )
    )

    accepted_count = result.scalar_one()

    if accepted_count >= shift.workers_needed:
        raise ValueError("Shift is fully staffed")

    result = await db.execute(
        select(Business.country_code).where(
            Business.id == shift.business_id
        )
    )

    country_code = result.scalar_one_or_none()

    if country_code is None:
        raise ValueError("Business country not found")

    if not await has_work_authorization(
        db,
        application.worker_profile_id,
        country_code,
        shift.ends_at,
    ):
        raise ValueError("Worker has no verified work authorization")

    if not await is_worker_available(
        db,
        application.worker_profile_id,
        shift.starts_at,
        shift.ends_at,
    ):
        raise ValueError("Worker is not available")

    if await has_shift_conflict(
        db,
        application.worker_profile_id,
        shift.starts_at,
        shift.ends_at,
    ):
        raise ValueError("Worker already has an overlapping shift")

    application.status = "accepted"

    await db.flush()

    return application