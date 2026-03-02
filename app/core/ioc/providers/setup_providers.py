from dishka import Provider

from .db_providers import ConfigProvider, PostgresSessionProvider, RedisProvider


def setup_providers() -> list[Provider]:
    providers = [
        ConfigProvider(),
        PostgresSessionProvider(),
        RedisProvider(),
    ]
    return providers
