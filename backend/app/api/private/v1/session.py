from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.worker_profile import WorkerProfile
from app.models.worker_skill import WorkerSkill
from app.models.worker_skill_preference import WorkerSkillPreference

router = APIRouter(prefix="/session", tags=["Shifts"])

@router.get("/me")
async def get_my_session(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    worker_profile = await db.scalar(
        select(WorkerProfile).where(
            WorkerProfile.user_id == user.id
        )
    )

    skills = []
    preferences = []

    if worker_profile:
        skills_result = await db.execute(
            select(WorkerSkill).where(
                WorkerSkill.worker_profile_id == worker_profile.id
            )
        )

        skills = [
            {
                "skill_id": skill.skill_id,
                "years_experience": skill.years_experience,
                "min_hourly_rate": skill.min_hourly_rate,
                "max_hourly_rate": skill.max_hourly_rate,
            }
            for skill in skills_result.scalars().all()
        ]

        preferences_result = await db.execute(
            select(WorkerSkillPreference.skill_id).where(
                WorkerSkillPreference.worker_profile_id == worker_profile.id
            )
        )

        preferences = preferences_result.scalars().all()

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "preferred_language": user.preferred_language,
        },
        "worker_profile": (
            {
                "id": worker_profile.id,
                "avatar_url": worker_profile.avatar_url,
                "bio": worker_profile.bio,
                "latitude": worker_profile.latitude,
                "longitude": worker_profile.longitude,
                "willing_to_travel": worker_profile.willing_to_travel,
            }
            if worker_profile
            else None
        ),
        "skills": skills,
        "preferences": preferences,
    }