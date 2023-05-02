"""Define reusable columns."""
import uuid
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID

from source.database.instance import db


def generate_uuid() -> db.Column:
    """Generate UUID primary key column.

    Returns
    -------
    SQLAlchemy.Column (UUID)
    """

    return db.Column(UUID(as_uuid=True), primary_key=True, server_default=str(uuid.uuid4()))


def created_at() -> db.Column:
    """Generate TIMESTAMP created_at column.

    Returns
    -------
    SQLAlchemy.Column (TIMESTAMP)
    """
    return db.Column(
        TIMESTAMP, nullable=False, server_onupdate=func.now(), server_default=func.now()
    )


def updated_at() -> db.Column:
    """Generate TIMESTAMP updated_at column.

    Returns
    -------
    SQLAlchemy.Column (TIMESTAMP)
    """
    return db.Column(
        TIMESTAMP, nullable=False, server_onupdate=func.now(), server_default=func.now()
    )


def deleted_at() -> db.Column:
    """Generate TIMESTAMP deleted_at column.

    Returns
    -------
    SQLAlchemy.Column (TIMESTAMP)
    """
    return db.Column(TIMESTAMP, nullable=True, server_default=None)
