import math

from fastapi import Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.models.job_shift import JobShift
from app.models.business import Business
from app.models.skill import Skill

router = APIRouter(prefix="/job-shifts", tags=["job_shifts"])

def distance_km(lat1, lon1, lat2, lon2):
    radius = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * radius * math.asin(min(1, math.sqrt(a)))


@router.get("/nearby")
async def get_nearby_jobs(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobShift, Business, Skill)
        .join(Business, JobShift.business_id == Business.id)
        .join(Skill, JobShift.skill_id == Skill.id)
        .where(
            JobShift.status == "open",
            Business.latitude.is_not(None),
            Business.longitude.is_not(None),
        )
    )

    jobs = []

    for shift, business, skill in result.all():
        distance = distance_km(
            latitude,
            longitude,
            business.latitude,
            business.longitude,
        )

        if distance > 50:
            continue

        jobs.append({
            "id": shift.id,
            "business_id": business.id,
            "business_name": business.name,
            "job_type": skill.code,
            "description": shift.description,
            "latitude": business.latitude,
            "longitude": business.longitude,
            "distance_km": round(distance, 1),
            "starts_at": shift.starts_at,
            "ends_at": shift.ends_at,
            "hourly_rate": shift.hourly_rate,
            "currency": shift.currency,
            "workers_needed": shift.workers_needed,
        })

    jobs.sort(key=lambda job: job["distance_km"])

    return jobs