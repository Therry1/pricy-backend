from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import selectors

from app.common.configs.settings import settings
from app.common.models.base import Base

print(">>> DATABASE_URL utilisée :", settings.DATABASE_URL)

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    async def run_async_migrations() -> None:
        connectable = create_async_engine(settings.DATABASE_URL)
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    include_schemas=True,           # ✅ ajouté
                    version_table_schema="public",  # ✅ ajouté
                )
            )
            await connection.exec_driver_sql("SET search_path TO public")  # ✅ ajouté
            await connection.run_sync(lambda conn: context.run_migrations())
            await connection.commit()  # ✅ commit explicite

        await connectable.dispose()

    asyncio.run(
        run_async_migrations(),
        loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()