from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import ROOT_DIR, settings


def resolve_sqlite_database_path(
    configured_path: str | Path | None = None,
) -> Path:
    database_path = Path(
        configured_path or settings.sqlite_db_path
    )

    if database_path.is_absolute():
        return database_path

    return (ROOT_DIR / database_path).resolve()


def build_sqlite_database_url(
    configured_path: str | Path | None = None,
) -> str:
    database_path = resolve_sqlite_database_path(
        configured_path
    )

    return f"sqlite:///{database_path.as_posix()}"


def create_database_engine(
    database_url: str | None = None,
) -> Engine:
    resolved_database_url = (
        database_url or build_sqlite_database_url()
    )

    connect_args: dict[str, object] = {}

    if resolved_database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        resolved_database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )


engine = create_database_engine()

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_database_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()