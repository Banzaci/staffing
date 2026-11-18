
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.auth.employer_access import require_business_access


@pytest.mark.asyncio
async def test_business_owner_has_access():
    user = MagicMock(id=uuid.uuid4())
    business = MagicMock(id=uuid.uuid4())

    result = MagicMock()
    result.scalar_one_or_none.return_value = business

    db = AsyncMock()
    db.execute.return_value = result

    response = await require_business_access(
        db,
        user,
        business.id,
    )

    assert response.id == business.id


@pytest.mark.asyncio
async def test_other_user_denied():
    user = MagicMock(id=uuid.uuid4())

    result = MagicMock()
    result.scalar_one_or_none.return_value = None

    db = AsyncMock()
    db.execute.return_value = result

    with pytest.raises(HTTPException) as exc:
        await require_business_access(
            db,
            user,
            uuid.uuid4(),
        )

    assert exc.value.status_code == 403
