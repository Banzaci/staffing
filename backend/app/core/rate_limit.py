
from redis.asyncio import Redis


RATE_LIMIT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return count
"""

async def check_rate_limit(
    redis: Redis,
    key: str,
    limit: int,
    window: int,
) -> bool:
    if limit <= 0 or window <= 0:
        raise ValueError("limit and window must be positive")

    count = await redis.eval(
        RATE_LIMIT_SCRIPT,
        1,
        key,
        window,
    )

    return int(count) <= limit
