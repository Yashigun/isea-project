from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Create a new SQLAlchemy database session.

    A fresh session is provided for every request and is
    automatically closed when the request finishes,
    regardless of whether it succeeds or raises an exception.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()