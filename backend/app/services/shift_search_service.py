
import math
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.job_shift import JobShift
from app.models.shift_application import ShiftApplication


async def search_shifts(
    db: AsyncSession,
    skill_id: uuid.UUID | None = None,
    country_code: str | None = None,
    starts_from: datetime | None = None,
    starts_before: datetime | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    radius_km: float | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[JobShift]:
    if (latitude is None) != (longitude is None):
        raise ValueError("Latitude and longitude must be provided together")

    if radius_km is not None:
        if latitude is None:
            raise ValueError("Coordinates are required for radius search")
        if not math.isfinite(radius_km) or radius_km <= 0:
            raise ValueError("Radius must be greater than zero")

    if latitude is not None:
        if not math.isfinite(latitude) or not -90 <= latitude <= 90:
            raise ValueError("Invalid latitude")
        if not math.isfinite(longitude) or not -180 <= longitude <= 180:
            raise ValueError("Invalid longitude")

    accepted_counts = (
        select(
            ShiftApplication.job_shift_id.label("shift_id"),
            func.count(ShiftApplication.id).label("accepted_count"),
        )
        .where(
            ShiftApplication.status == "accepted",
            ShiftApplication.deleted_at.is_(None),
        )
        .group_by(ShiftApplication.job_shift_id)
        .subquery()
    )

    stmt = (
        select(JobShift)
        .join(Business, Business.id == JobShift.business_id)
        .outerjoin(
            accepted_counts,
            accepted_counts.c.shift_id == JobShift.id,
        )
        .where(
            JobShift.status == "open",
            JobShift.starts_at > datetime.now(timezone.utc),
            func.coalesce(
                accepted_counts.c.accepted_count, 0
            ) < JobShift.workers_needed,
        )
    )

    if skill_id is not None:
        stmt = stmt.where(JobShift.skill_id == skill_id)

    if country_code is not None:
        stmt = stmt.where(
            Business.country_code == country_code.upper()
        )

    if starts_from is not None:
        stmt = stmt.where(JobShift.starts_at >= starts_from)

    if starts_before is not None:
        stmt = stmt.where(JobShift.starts_at < starts_before)

    if latitude is not None:
        lat1 = func.radians(latitude)
        lat2 = func.radians(Business.latitude)
        delta_lat = func.radians(Business.latitude - latitude)
        delta_lon = func.radians(Business.longitude - longitude)

        a = (
            func.power(func.sin(delta_lat / 2), 2)
            + func.cos(lat1)
            * func.cos(lat2)
            * func.power(func.sin(delta_lon / 2), 2)
        )

        distance_km = (
            6371.0
            * 2
            * func.asin(func.sqrt(func.least(1.0, func.greatest(0.0, a))))
        )

        stmt = stmt.where(
            Business.latitude.is_not(None),
            Business.longitude.is_not(None),
        )

        if radius_km is not None:
            stmt = stmt.where(distance_km <= radius_km)

        stmt = stmt.order_by(
            distance_km.asc(),
            JobShift.starts_at.asc(),
            JobShift.id.asc(),
        )
    else:
        stmt = stmt.order_by(
            JobShift.starts_at.asc(),
            JobShift.id.asc(),
        )

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)
    return list(result.scalars().all())
