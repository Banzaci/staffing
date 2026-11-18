
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.shift_conflicts import has_shift_conflict


@pytest.mark.asyncio
async def test_shift_conflict_found():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = uuid.uuid4()
    db.execute.return_value = result

    starts_at = datetime(2026, 12, 1, 9, tzinfo=timezone.utc)

    conflict = await has_shift_conflict(
        db,
        uuid.uuid4(),
        starts_at,
        starts_at + timedelta(hours=3),
    )

    assert conflict is True


@pytest.mark.asyncio
async def test_no_shift_conflict():
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db.execute.return_value = result

    starts_at = datetime(2026, 12, 1, 12, tzinfo=timezone.utc)

    conflict = await has_shift_conflict(
        db,
        uuid.uuid4(),
        starts_at,
        starts_at + timedelta(hours=3),
    )

    assert conflict is False


@pytest.mark.asyncio
async def test_invalid_shift_time():
    db = AsyncMock()
    starts_at = datetime(2026, 12, 1, 12, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        await has_shift_conflict(
            db,
            uuid.uuid4(),
            starts_at,
            starts_at,
        )

    db.execute.assert_not_called()
