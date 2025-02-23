import os
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alembic configuration object
config = context.config

# Set up logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Database credentials from .env
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "dbname")

# Async database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set sqlalchemy.url dynamically
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import models
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Base  # Ensure this matches your actual models file location
target_metadata = Base.metadata



target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
