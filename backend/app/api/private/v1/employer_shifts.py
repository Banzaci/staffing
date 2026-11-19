
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.business import Business
from app.models.employer import Employer
from app.models.shift_application import ShiftApplication
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

@router.get("")
async def get_employer_shifts(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(JobShift)
        .join(Business, JobShift.business_id == Business.id)
        .join(Employer, Business.employer_id == Employer.id)
        .where(Employer.user_id == user.id)
        .order_by(JobShift.starts_at.desc())
    )

    shifts = result.scalars().all()

    if not shifts:
        return []

    applications_result = await db.execute(
        select(ShiftApplication)
        .where(
            ShiftApplication.job_shift_id.in_(
                [shift.id for shift in shifts]
            ),
            ShiftApplication.deleted_at.is_(None),
        )
        .order_by(ShiftApplication.created_at.desc())
    )

    applications_by_shift = {shift.id: [] for shift in shifts}

    for application in applications_result.scalars().all():
        applications_by_shift[application.job_shift_id].append({
            "id": application.id,
            "worker_profile_id": application.worker_profile_id,
            "status": application.status,
            "created_at": application.created_at,
        })

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
            "status": shift.status,
            "applications": applications_by_shift[shift.id],
        }
        for shift in shifts
    ]