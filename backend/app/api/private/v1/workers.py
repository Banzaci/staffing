import uuid

from pydantic import BaseModel
from sqlalchemy import delete

from app.models.skill import Skill
from app.models.worker_skill_preference import WorkerSkillPreference
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shift_application import ShiftApplication
from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.worker_profile import WorkerProfile
from app.schemas.worker_profile import WorkerProfileCreate
from app.schemas.worker_preferences import WorkerPreferencesUpdate

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.get("/me/preferences")
async def get_my_preferences(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    worker = await db.scalar(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user.id
        )
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker profile not found",
        )

    result = await db.execute(
        select(WorkerSkillPreference.skill_id).where(
            WorkerSkillPreference.worker_profile_id == worker.id
        )
    )

    return {"skill_ids": result.scalars().all()}

@router.put("/me/preferences")
async def update_my_preferences(
    payload: WorkerPreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    worker = await db.scalar(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user.id
        )
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker profile not found",
        )

    skill_ids = list(dict.fromkeys(payload.skill_ids))

    if skill_ids:
        result = await db.execute(
            select(Skill.id).where(Skill.id.in_(skill_ids))
        )

        existing_ids = set(result.scalars().all())

        if len(existing_ids) != len(skill_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more skills do not exist",
            )

    await db.execute(
        delete(WorkerSkillPreference).where(
            WorkerSkillPreference.worker_profile_id == worker.id
        )
    )

    db.add_all(
        [
            WorkerSkillPreference(
                worker_profile_id=worker.id,
                skill_id=skill_id,
            )
            for skill_id in skill_ids
        ]
    )

    await db.commit()

    return {"skill_ids": skill_ids}

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

@router.get("/me/applications")
async def get_my_shift_applications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ShiftApplication)
        .join(
            WorkerProfile,
            ShiftApplication.worker_profile_id == WorkerProfile.id,
        )
        .where(
            WorkerProfile.user_id == user.id,
            ShiftApplication.deleted_at.is_(None),
        )
        .order_by(ShiftApplication.created_at.desc())
    )

    applications = result.scalars().all()

    return [
        {
            "id": application.id,
            "job_shift_id": application.job_shift_id,
            "status": application.status,
            "created_at": application.created_at,
        }
        for application in applications
    ]