import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.conf.config import config

class DatabaseSessionManager:
    """A session manager for handling database connections using SQLAlchemy's async engine.

    This class provides an asynchronous context manager for creating and managing database sessions,
    with support for automatic connection and transaction handling.

    Attributes:
        _engine (AsyncEngine): An asynchronous SQLAlchemy engine for database connections.
        _session_maker (async_sessionmaker): A factory for creating asynchronous database sessions.
    """
    def __init__(self, url: str):
        """Initialize the DatabaseSessionManager with a database connection URL.

        Args:
            url (str): The database connection URL, typically from configuration.
        """
        self._engine: AsyncEngine = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """An asynchronous context manager for creating and managing database sessions.

        This method provides a safe way to create a database session with automatic
        rollback in case of SQLAlchemy errors and ensures the session is always closed.

        Yields:
            AsyncSession: An asynchronous database session.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        async with self._session_maker() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)

async def get_db():
    """An asynchronous generator function to provide database sessions.

    This function is typically used as a dependency in FastAPI or similar async web frameworks
    to provide a database session for each request.

    Yields:
        AsyncSession: An asynchronous database session that can be used for database operations.
    """
    async with sessionmanager.session() as session:
        yield session
