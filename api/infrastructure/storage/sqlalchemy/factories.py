from typing import AsyncGenerator, Type

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.config import Settings


def build_sa_engine(
    settings: Settings,
) -> AsyncEngine:
    engine = create_async_engine(settings.database.url)
    return engine


def build_sa_session_factory(
    engine: AsyncEngine,
    class_: Type[AsyncSession] = AsyncSession,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, class_=class_, expire_on_commit=False
    )


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
