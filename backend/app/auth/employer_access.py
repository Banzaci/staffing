
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.employer import Employer
from app.models.user import User


async def require_business_access(
    db: AsyncSession,
    user: User,
    business_id: uuid.UUID,
) -> Business:
    result = await db.execute(
        select(Business)
        .join(Employer, Business.employer_id == Employer.id)
        .where(
            Business.id == business_id,
            Employer.user_id == user.id,
        )
    )

    business = result.scalar_one_or_none()

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this business",
        )

    return business
