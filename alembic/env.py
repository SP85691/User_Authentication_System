from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

# Import your models
import models

config = context.config
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

# Setup Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Initialize your models
target_metadata = models.Base.metadata

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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

            # Create tables using op.create_all()
            engine = create_engine(os.environ["DATABASE_URL"])
            models.Base.metadata.create_all(bind=engine)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
