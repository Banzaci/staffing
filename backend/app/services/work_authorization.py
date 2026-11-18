
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.worker_work_authorization import WorkerWorkAuthorization


async def has_work_authorization(
    db: AsyncSession,
    worker_profile_id: uuid.UUID,
    country_code: str,
    shift_ends_at: datetime,
) -> bool:
    if shift_ends_at.tzinfo is None:
        raise ValueError("Shift end must have a timezone")

    stmt = (
        select(WorkerWorkAuthorization.id)
        .where(
            WorkerWorkAuthorization.worker_profile_id == worker_profile_id,
            WorkerWorkAuthorization.country_code == country_code.upper(),
            WorkerWorkAuthorization.verification_status == "verified",
            WorkerWorkAuthorization.authorization_type.in_(
                ["citizen", "permanent_resident", "work_permit", "other"]
            ),
            (
                WorkerWorkAuthorization.expires_at.is_(None)
                | (
                    WorkerWorkAuthorization.expires_at
                    >= shift_ends_at.date()
                )
            ),
        )
        .limit(1)
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None
