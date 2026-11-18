
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.worker_availability import WorkerAvailability


async def is_worker_available(
    db: AsyncSession,
    worker_profile_id: uuid.UUID,
    starts_at: datetime,
    ends_at: datetime,
) -> bool:
    if starts_at >= ends_at:
        raise ValueError("Shift end must be after start")

    stmt = (
        select(WorkerAvailability.id)
        .where(
            WorkerAvailability.worker_profile_id == worker_profile_id,
            WorkerAvailability.deleted_at.is_(None),
            WorkerAvailability.starts_at <= starts_at,
            WorkerAvailability.ends_at >= ends_at,
        )
        .limit(1)
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none() is not None
