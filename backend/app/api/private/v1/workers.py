
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.worker_profile import WorkerProfile
from app.schemas.worker_profile import WorkerProfileCreate

router = APIRouter(prefix="/workers", tags=["Workers"])


@router.post("", status_code=201)
async def create_worker_profile(
    payload: WorkerProfileCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user.id
        )
    )

    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=409,
            detail="Worker profile already exists",
        )

    worker = WorkerProfile(
        user_id=user.id,
        bio=payload.bio,
        avatar_url=payload.avatar_url,
        latitude=payload.latitude,
        longitude=payload.longitude,
        willing_to_travel=payload.willing_to_travel,
    )

    db.add(worker)

    try:
        await db.commit()
        await db.refresh(worker)
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Worker profile already exists",
        ) from exc

    return {
        "id": worker.id,
        "user_id": worker.user_id,
        "bio": worker.bio,
        "avatar_url": worker.avatar_url,
        "latitude": worker.latitude,
        "longitude": worker.longitude,
        "willing_to_travel": worker.willing_to_travel,
    }


@router.get("/me")
async def get_my_worker_profile(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user.id
        )
    )

    worker = result.scalar_one_or_none()

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker profile not found",
        )

    return {
        "id": worker.id,
        "user_id": worker.user_id,
        "bio": worker.bio,
        "avatar_url": worker.avatar_url,
        "latitude": worker.latitude,
        "longitude": worker.longitude,
        "willing_to_travel": worker.willing_to_travel,
    }
