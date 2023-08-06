from contextvars import ContextVar, Token
from typing import AsyncGenerator
from uuid import uuid4

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.requests import Request
from yarl import URL

from vulcan.core.utils import logger
from vulcan.core.config import config

session_context: ContextVar[str] = ContextVar("session_context")

Base = declarative_base()


def build_db_url() -> URL:
    """
    Assemble database URL from settings.

    :return: database URL.
    """
    return URL.build(
        scheme="postgresql+asyncpg",
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
        path=f"/{config.DB_DATABASE}",
    )


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def get_session_context() -> str:
    return session_context.get()


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application."""
    engine = create_async_engine(str(build_db_url()), echo=True, pool_recycle=3600)

    session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=get_session_context,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session_id = str(uuid4())
    session: AsyncSession = request.app.state.db_session_factory()
    context = set_session_context(session_id=session_id)
    logger.trace("get_db_session: " + str(session))

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.remove()
        reset_session_context(context=context)
