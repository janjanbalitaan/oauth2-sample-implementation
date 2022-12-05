from databases import Database
from sqlalchemy import (
    Column,
    MetaData,
    create_engine,
    String,
    Table,
    DateTime,
    ForeignKeyConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from .settings import Settings


settings = Settings()

engine = create_engine(settings.db_uri)
metadata = MetaData(engine)

# run a script to install extension for generate uuid 4 in postgresql
with engine.connect() as conn:
    raw_sql = conn.execute(
        'create extension if not exists "uuid-ossp";'
    )

# TODO: update all datetime to utc time later on
# this will be generic columns that can be used across all tables
def base_columns():
    return {
        Column('created', DateTime, nullable=False, server_default=text("NOW()")),
        Column('updated', DateTime, nullable=False, server_default=text("NOW()"), onupdate=text("NOW()")),
        # add this, may we want to implement non-force delete rows later on 
        Column('deleted', DateTime, nullable=True),
    }

users = Table(
    'users',
    metadata,
    *base_columns(),
    Column('id', UUID, primary_key=True, unique=True, nullable=False, server_default=text("uuid_generate_v4()")),
    Column('username', String(50), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
)

tokens = Table(
    'tokens',
    metadata,
    *base_columns(),
    # TODO: change the token to a much unique implementation
    Column('token', UUID, primary_key=True, unique=True, nullable=False, server_default=text("uuid_generate_v4()")),
    # can set to non-expiry token if value is null
    # TODO: set a manual expiration and use environment variable to dynamically set the interval
    Column('expiration', DateTime, nullable=True, server_default=text("NOW() + INTERVAL '30 DAY'")),
    Column('user_id', UUID, nullable=False),
    ForeignKeyConstraint(["user_id"], [users.c.id], ondelete="CASCADE"),
)

database = Database(settings.db_uri)

