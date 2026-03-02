from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_CONFIG = dict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
    populate_by_name=True,
    protected_namespaces=(),
)


class ProjectBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(**_BASE_CONFIG)


class PostgresSettings(ProjectBaseSettings):
    host: str = Field(min_length=1)
    port: int = Field(gt=0, le=65535)
    user: str = Field(min_length=1)
    password: str = Field(min_length=1)
    database: str = Field(min_length=1)
    pool_size: int = Field(default=15, gt=0)
    max_overflow: int = Field(default=15, ge=0)
    echo: bool = Field(default=False)

    model_config = SettingsConfigDict(**_BASE_CONFIG, env_prefix="POSTGRES_")

    def async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class RedisSettings(ProjectBaseSettings):
    host: str = Field(min_length=1)
    port: int = Field(gt=0, le=65535)
    password: str = Field(default="")
    database: int = Field(ge=0, le=15)

    model_config = SettingsConfigDict(**_BASE_CONFIG, env_prefix="REDIS_")

    def url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.database}"


class Config(ProjectBaseSettings):
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
