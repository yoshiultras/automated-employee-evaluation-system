import asyncio
from logging.config import fileConfig

from alembic import context
from api.config import Settings
from api.infrastructure.storage.sqlalchemy.models.base import BaseModel
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

setting = Settings()
db_settings = setting.database
config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    url = db_settings.url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    if configuration is not None:
        configuration["sqlalchemy.url"] = db_settings.url
    else:
        raise ValueError("Configuration is None")

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
