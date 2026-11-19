
import uuid
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.skill import Skill
from app.models.worker_profile import WorkerProfile
from app.models.worker_skill import WorkerSkill
from app.models.skill_translation import SkillTranslation
from app.schemas.skills import WorkerSkillInput

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.put("/{skill_id}/me")
async def save_my_skill(
    skill_id: uuid.UUID,
    payload: WorkerSkillInput,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await db.scalar(
        select(WorkerProfile).where(WorkerProfile.user_id == user.id)
    )

    if profile is None:
        raise HTTPException(status_code=404, detail="Worker profile not found")

    skill = await db.get(Skill, skill_id)

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    if (
        payload.min_hourly_rate is not None
        and payload.max_hourly_rate is not None
        and payload.min_hourly_rate > payload.max_hourly_rate
    ):
        raise HTTPException(status_code=422, detail="Invalid hourly rate range")

    worker_skill = await db.scalar(
        select(WorkerSkill).where(
            WorkerSkill.worker_profile_id == profile.id,
            WorkerSkill.skill_id == skill_id,
        )
    )

    if worker_skill is None:
        worker_skill = WorkerSkill(
            worker_profile_id=profile.id,
            skill_id=skill_id,
        )
        db.add(worker_skill)

    worker_skill.years_experience = payload.years_experience
    worker_skill.min_hourly_rate = payload.min_hourly_rate
    worker_skill.max_hourly_rate = payload.max_hourly_rate

    await db.commit()
    await db.refresh(worker_skill)

    return {
        "skill_id": worker_skill.skill_id,
        "years_experience": worker_skill.years_experience,
        "min_hourly_rate": worker_skill.min_hourly_rate,
        "max_hourly_rate": worker_skill.max_hourly_rate,
    }


@router.delete("/{skill_id}/me", status_code=204)
async def delete_my_skill(
    skill_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await db.scalar(
        select(WorkerProfile).where(WorkerProfile.user_id == user.id)
    )

    if profile is None:
        raise HTTPException(status_code=404, detail="Worker profile not found")

    worker_skill = await db.scalar(
        select(WorkerSkill).where(
            WorkerSkill.worker_profile_id == profile.id,
            WorkerSkill.skill_id == skill_id,
        )
    )

    if worker_skill is None:
        raise HTTPException(status_code=404, detail="Worker skill not found")

    await db.delete(worker_skill)
    await db.commit()

@router.get("")
async def list_skills(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(
            Skill.id,
            Skill.code,
            SkillTranslation.language_code,
            SkillTranslation.name,
        )
        .outerjoin(
            SkillTranslation,
            SkillTranslation.skill_id == Skill.id,
        )
        .order_by(Skill.code, SkillTranslation.language_code)
    )

    skills = {}

    for skill_id, code, language_code, name in result.all():
        if skill_id not in skills:
            skills[skill_id] = {
                "id": skill_id,
                "code": code,
                "translations": {},
            }

        if language_code is not None:
            skills[skill_id]["translations"][language_code] = name

    return list(skills.values())