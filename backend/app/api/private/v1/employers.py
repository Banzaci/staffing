
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.employer import Employer
from app.models.user import User

router = APIRouter(prefix="/employers", tags=["Employers"])


@router.post("", status_code=201)
async def create_employer(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Employer).where(Employer.user_id == user.id)
    )

    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=409,
            detail="Employer profile already exists",
        )

    employer = Employer(user_id=user.id)
    db.add(employer)

    try:
        await db.commit()
        await db.refresh(employer)
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employer profile already exists",
        ) from exc

    return {
        "id": employer.id,
        "user_id": employer.user_id,
    }


@router.get("/me")
async def get_my_employer(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Employer).where(Employer.user_id == user.id)
    )

    employer = result.scalar_one_or_none()

    if employer is None:
        raise HTTPException(
            status_code=404,
            detail="Employer profile not found",
        )

    return {
        "id": employer.id,
        "user_id": employer.user_id,
    }
