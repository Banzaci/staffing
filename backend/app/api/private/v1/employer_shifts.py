
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.employer_access import require_business_access
from app.db.session import get_db
from app.models.job_shift import JobShift
from app.models.user import User
from app.schemas.job_shift import JobShiftCreate

router = APIRouter(prefix="/employer/shifts", tags=["Employer Shifts"])


@router.post("", status_code=201)
async def create_job_shift(
    payload: JobShiftCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await require_business_access(
        db=db,
        user=user,
        business_id=payload.business_id,
    )

    shift = JobShift(
        business_id=payload.business_id,
        skill_id=payload.skill_id,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        hourly_rate=payload.hourly_rate,
        currency=payload.currency.upper(),
        workers_needed=payload.workers_needed,
        status="open",
    )

    db.add(shift)

    try:
        await db.commit()
        await db.refresh(shift)
    except Exception:
        await db.rollback()
        raise

    return {
        "id": shift.id,
        "business_id": shift.business_id,
        "skill_id": shift.skill_id,
        "starts_at": shift.starts_at,
        "ends_at": shift.ends_at,
        "hourly_rate": shift.hourly_rate,
        "currency": shift.currency,
        "workers_needed": shift.workers_needed,
        "status": shift.status,
    }
