
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.shift_application_service import withdraw_shift_application
from app.auth.dependencies import get_current_user
from app.auth.employer_access import require_business_access
from app.db.session import get_db
from app.models.job_shift import JobShift
from app.models.shift_application import ShiftApplication
from app.models.user import User
from app.services.shift_approval import approve_shift_application

router = APIRouter(prefix="/shift-applications", tags=["Shift Applications"])

@router.post("/{application_id}/approve")
async def approve_application(
    application_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(ShiftApplication, JobShift)
        .join(JobShift, ShiftApplication.job_shift_id == JobShift.id)
        .where(
            ShiftApplication.id == application_id,
            ShiftApplication.deleted_at.is_(None),
        )
    )

    row = result.one_or_none()

    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")

    application, shift = row

    await require_business_access(db, user, shift.business_id)

    try:
        approved = await approve_shift_application(db, application.id)
        await db.commit()
    except ValueError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "id": str(approved.id),
        "status": approved.status,
    }

@router.post("/{application_id}/reject")
async def reject_application(
    application_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(ShiftApplication, JobShift)
        .join(JobShift, ShiftApplication.job_shift_id == JobShift.id)
        .where(
            ShiftApplication.id == application_id,
            ShiftApplication.deleted_at.is_(None),
        )
        .with_for_update(of=ShiftApplication)
    )

    row = result.one_or_none()

    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")

    application, shift = row

    try:
        await require_business_access(db, user, shift.business_id)

        if application.status != "pending":
            raise HTTPException(
                status_code=400,
                detail="Only pending applications can be rejected",
            )

        application.status = "rejected"

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return {
        "id": str(application.id),
        "status": application.status,
    }

@router.post("/{application_id}/withdraw")
async def withdraw_application(
    application_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        application = await withdraw_shift_application(
            db=db,
            user_id=user.id,
            application_id=application_id,
        )

        await db.commit()

        return {
            "id": application.id,
            "status": application.status,
        }

    except ValueError as exc:
        await db.rollback()

        if str(exc) == "Application not found":
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc