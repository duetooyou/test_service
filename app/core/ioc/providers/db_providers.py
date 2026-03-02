from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import new_session_maker, new_redis_client
from app.core.config import Config, PostgresSettings, RedisSettings


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_postgres_settings(self, config: Config) -> PostgresSettings:
        return config.postgres

    @provide(scope=Scope.APP)
    def get_redis_settings(self, config: Config) -> RedisSettings:
        return config.redis


class PostgresSessionProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self, config: PostgresSettings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with maker() as session:
            yield session


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis(self, config: RedisSettings) -> Redis:
        return new_redis_client(config)
