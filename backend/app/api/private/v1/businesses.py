
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.business import Business
from app.models.employer import Employer
from app.models.user import User
from app.schemas.business import BusinessCreate

router = APIRouter(prefix="/businesses", tags=["Businesses"])


@router.post("", status_code=201)
async def create_business(
    payload: BusinessCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Employer).where(Employer.user_id == user.id)
    )

    employer = result.scalar_one_or_none()

    if employer is None:
        raise HTTPException(
            status_code=403,
            detail="Employer profile required",
        )

    business = Business(
        employer_id=employer.id,
        name=payload.name,
        business_type_id=payload.business_type_id,
        country_code=payload.country_code.upper(),
        latitude=payload.latitude,
        longitude=payload.longitude,
    )

    db.add(business)

    try:
        await db.commit()
        await db.refresh(business)
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid business type or business data",
        ) from exc

    return {
        "id": business.id,
        "employer_id": business.employer_id,
        "name": business.name,
        "business_type_id": business.business_type_id,
        "country_code": business.country_code,
        "latitude": business.latitude,
        "longitude": business.longitude,
    }
