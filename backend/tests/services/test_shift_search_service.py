
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.dialects import postgresql

from app.services.shift_search_service import search_shifts


@pytest.mark.asyncio
async def test_search_shifts():
    shift = MagicMock()
    shift.id = uuid.uuid4()

    db = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = [shift]
    db.execute.return_value = result

    shifts = await search_shifts(db)

    assert shifts == [shift]
    db.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_search_shifts_filters():
    db = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = []
    db.execute.return_value = result

    skill_id = uuid.uuid4()
    starts_from = datetime.now(timezone.utc) + timedelta(days=1)
    starts_before = starts_from + timedelta(days=7)

    await search_shifts(
        db,
        skill_id=skill_id,
        country_code="ph",
        starts_from=starts_from,
        starts_before=starts_before,
        limit=20,
        offset=10,
    )

    stmt = db.execute.await_args.args[0]

    compiled = stmt.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True},
    )
    sql = str(compiled)

    assert str(skill_id) in sql
    assert "'PH'" in sql
    assert "LIMIT 20" in sql
    assert "OFFSET 10" in sql
    assert "accepted_count" in sql



@pytest.mark.asyncio
async def test_search_shifts_distance_filter():
    db = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = []
    db.execute.return_value = result

    await search_shifts(
        db,
        latitude=9.7845,
        longitude=126.1589,
        radius_km=20,
    )

    stmt = db.execute.await_args.args[0]

    sql = str(
        stmt.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    ).lower()

    assert "asin" in sql
    assert "radians" in sql
    assert "12742" in sql
    assert "20" in sql
    assert "order by" in sql
