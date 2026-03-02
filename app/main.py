from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dishka import make_async_container, FromDishka
from dishka.integrations.fastapi import setup_dishka as fastapi_integration, inject

from app.core.ioc.providers import setup_providers
from app.core.config import Config

config = Config()
container = make_async_container(*setup_providers(), context={Config: config})


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await container.close()


fastapi_app = FastAPI(name="Test Service", lifespan=lifespan)
fastapi_integration(container=container, app=fastapi_app)

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
