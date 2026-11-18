
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_shift import JobShift
from app.models.shift_application import ShiftApplication


async def has_shift_conflict(
    db: AsyncSession,
    worker_profile_id: uuid.UUID,
    starts_at: datetime,
    ends_at: datetime,
) -> bool:
    if starts_at >= ends_at:
        raise ValueError("Shift end must be after start")

    stmt = (
        select(ShiftApplication.id)
        .join(JobShift, ShiftApplication.job_shift_id == JobShift.id)
        .where(
            ShiftApplication.worker_profile_id == worker_profile_id,
            ShiftApplication.status == "accepted",
            ShiftApplication.deleted_at.is_(None),
            JobShift.status != "cancelled",
            JobShift.starts_at < ends_at,
            JobShift.ends_at > starts_at,
        )
        .limit(1)
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none() is not None
