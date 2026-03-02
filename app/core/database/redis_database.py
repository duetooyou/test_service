from redis.asyncio import Redis

from app.core.config import RedisSettings


def new_redis_client(redis_config: RedisSettings) -> Redis:
    return Redis.from_url(
        redis_config.url(),
        decode_responses=True,
    )
