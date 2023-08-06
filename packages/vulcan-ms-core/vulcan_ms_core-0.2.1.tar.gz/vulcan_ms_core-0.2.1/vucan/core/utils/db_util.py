from typing import AsyncGenerator

from core.util import config_env, logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from yarl import URL


def build_db_url() -> URL:
    """
    Assemble database URL from settings.

    :return: database URL.
    """
    return URL.build(
        scheme="postgresql+asyncpg",
        host=config_env.load("DB_HOST"),
        port=config_env.load("DB_PORT"),
        user=config_env.load("DB_USER"),
        password=config_env.load("DB_PASS"),
        path=f"/{config_env.load('DB_DATABASE')}",
    )


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    logger.trace("get_db_session: " + str(session))

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()
