from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.core.config import PostgresSettings


def new_session_maker(psql_config: PostgresSettings) -> async_sessionmaker[AsyncSession]:
    database_uri = psql_config.async_url()

    engine = create_async_engine(
        database_uri,
        pool_size=psql_config.pool_size,
        max_overflow=psql_config.max_overflow,
        echo=psql_config.echo,
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
