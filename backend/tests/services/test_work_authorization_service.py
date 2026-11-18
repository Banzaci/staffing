
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.work_authorization import has_work_authorization


@pytest.mark.asyncio
async def test_verified_work_authorization():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = uuid.uuid4()
    db.execute.return_value = result

    authorized = await has_work_authorization(
        db,
        uuid.uuid4(),
        "PH",
        datetime(2026, 12, 1, tzinfo=timezone.utc),
    )

    assert authorized is True


@pytest.mark.asyncio
async def test_missing_work_authorization():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db.execute.return_value = result

    authorized = await has_work_authorization(
        db,
        uuid.uuid4(),
        "GH",
        datetime(2026, 12, 1, tzinfo=timezone.utc),
    )

    assert authorized is False
