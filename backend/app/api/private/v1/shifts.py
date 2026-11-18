
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from fastapi import Query
from app.services.shift_search_service import search_shifts
from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.shift_application_service import apply_for_shift

router = APIRouter(prefix="/shifts", tags=["Shifts"])

@router.post("/{shift_id}/apply", status_code=201)
async def apply_to_shift(
    shift_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        application = await apply_for_shift(
            db=db,
            user_id=user.id,
            shift_id=shift_id,
        )

        await db.commit()

        return {
            "id": application.id,
            "job_shift_id": application.job_shift_id,
            "status": application.status,
        }

    except ValueError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Worker has already applied",
        ) from exc



@router.get("")
async def list_available_shifts(
    skill_id: uuid.UUID | None = None,
    country_code: str | None = Query(
        default=None, min_length=2, max_length=2
    ),
    starts_from: datetime | None = None,
    starts_before: datetime | None = None,
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
    radius_km: float | None = Query(default=None, gt=0, le=500),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if (latitude is None) != (longitude is None):
        raise HTTPException(
            status_code=422,
            detail="Latitude and longitude must be provided together",
        )

    if radius_km is not None and latitude is None:
        raise HTTPException(
            status_code=422,
            detail="Coordinates are required for radius search",
        )

    if starts_from is not None and starts_from.tzinfo is None:
        raise HTTPException(
            status_code=422,
            detail="starts_from must include a timezone",
        )

    if starts_before is not None and starts_before.tzinfo is None:
        raise HTTPException(
            status_code=422,
            detail="starts_before must include a timezone",
        )

    shifts = await search_shifts(
        db=db,
        skill_id=skill_id,
        country_code=country_code,
        starts_from=starts_from,
        starts_before=starts_before,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        limit=limit,
        offset=offset,
    )

    return [
        {
            "id": shift.id,
            "business_id": shift.business_id,
            "skill_id": shift.skill_id,
            "starts_at": shift.starts_at,
            "ends_at": shift.ends_at,
            "hourly_rate": shift.hourly_rate,
            "currency": shift.currency,
            "workers_needed": shift.workers_needed,
        }
        for shift in shifts
    ]

