
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.worker_availability import is_worker_available


@pytest.mark.asyncio
async def test_worker_available():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = uuid.uuid4()
    db.execute.return_value = result

    start = datetime(2026, 12, 1, 9, tzinfo=timezone.utc)

    available = await is_worker_available(
        db,
        uuid.uuid4(),
        start,
        start + timedelta(hours=3),
    )

    assert available is True


@pytest.mark.asyncio
async def test_worker_unavailable():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db.execute.return_value = result

    start = datetime(2026, 12, 1, 9, tzinfo=timezone.utc)

    available = await is_worker_available(
        db,
        uuid.uuid4(),
        start,
        start + timedelta(hours=3),
    )

    assert available is False


@pytest.mark.asyncio
async def test_invalid_availability_time():
    db = AsyncMock()
    start = datetime(2026, 12, 1, 9, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        await is_worker_available(
            db,
            uuid.uuid4(),
            start,
            start,
        )

    db.execute.assert_not_called()
