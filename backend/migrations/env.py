from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection

from app.db.base import Base
from app.db.session import (
    build_sqlite_database_url,
    engine,
)
from app.models import ProductModel  # noqa: F401


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

MANAGED_TABLE_NAMES = set(target_metadata.tables)


def include_object(
    object_: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    del object_, compare_to

    if (
        type_ == "table"
        and reflected
        and name not in MANAGED_TABLE_NAMES
    ):
        return False

    return True


def configure_migration_context(
    connection: Connection,
) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,
        include_object=include_object,
    )


def run_migrations_offline() -> None:
    context.configure(
        url=build_sqlite_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        render_as_batch=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        configure_migration_context(connection)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()