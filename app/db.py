
import os
from sqlalchemy import create_engine


from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel

POSTGRES_URL = os.environ.get("DATABASE_URL_UNPOOLED")


_engine = None


def get_engine() -> Engine:
    global _engine
    if _engine is not None:
        return _engine

    if not POSTGRES_URL:
        raise RuntimeError("POSTGRES_URL is not set")
    
    _engine = create_engine(POSTGRES_URL)
    return _engine


def create_all() -> None:
    """Creates all database tables."""
    try:
        from app.schema import Message  # noqa

        SQLModel.metadata.create_all(get_engine())
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to create database tables: {str(e)}") from e


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Provides a transactional scope around a series of operations.
    Automatically rolls back failed transactions and closes the session.
    """
    session = Session(get_engine())
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}") from e
    finally:
        session.close()
