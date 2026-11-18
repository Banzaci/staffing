
from fastapi import APIRouter, Depends, HTTPException, Request
from redis.asyncio import Redis

from app.core.rate_limit import check_rate_limit
from app.core.redis import get_redis

router = APIRouter()


@router.get("/health")
async def health(
    request: Request,
    redis: Redis = Depends(get_redis),
):
    client_ip = request.client.host if request.client else "unknown"

    allowed = await check_rate_limit(
        redis=redis,
        key=f"rate_limit:health:{client_ip}",
        limit=10,
        window=60,
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

    return {"status": "ok"}
