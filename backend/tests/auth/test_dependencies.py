
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_get_current_user():
    user_id = uuid.uuid4()
    user = MagicMock(id=user_id, is_active=True)

    result = MagicMock()
    result.scalar_one_or_none.return_value = user

    db = AsyncMock()
    db.execute.return_value = result

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=create_access_token(user_id),
    )

    current_user = await get_current_user(credentials, db)

    assert current_user.id == user_id


@pytest.mark.asyncio
async def test_missing_token():
    db = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await get_current_user(None, db)

    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token():
    db = AsyncMock()

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid",
    )

    with pytest.raises(HTTPException) as exc:
        await get_current_user(credentials, db)

    assert exc.value.status_code == 401
