from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session.

    A new database session is created for each request and is
    always closed after the request finishes, even if an
    exception occurs.
    """

    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()