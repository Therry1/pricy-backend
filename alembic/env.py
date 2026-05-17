from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
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


def include_object(object, name, type_, reflected, compare_to):
    """Exclure les tables internes d'Alembic de l'autogenerate."""
    if type_ == "table" and name == "alembic_version":
        return False
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    async def run_async_migrations() -> None:
        connectable = create_async_engine(settings.DATABASE_URL)

        async with connectable.connect() as connection:
            await connection.exec_driver_sql("SET search_path TO public")

            def do_migrations(conn):
                context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    include_schemas=True,
                    version_table_schema="public",
                    include_object=include_object,
                )
                context.run_migrations()

            await connection.run_sync(do_migrations)
            await connection.commit()

        await connectable.dispose()

    asyncio.run(
        run_async_migrations(),
        loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()