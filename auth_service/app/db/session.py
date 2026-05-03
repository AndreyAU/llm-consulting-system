from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def build_sqlite_url(sqlite_path: str) -> str:
    return f"sqlite+aiosqlite:///{sqlite_path}"


engine = create_async_engine(
    build_sqlite_url(settings.SQLITE_PATH),
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
