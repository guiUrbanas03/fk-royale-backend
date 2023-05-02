"""Create users table.

Revision ID: 8d2fffd52f76
Revises:
Create Date: 2023-02-06 10:36:12.651284
"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import USERS_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "8d2fffd52f76"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table structure."""
    op.create_table(
        USERS_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("email", sa.String(300), unique=True, nullable=False),
        sa.Column("password", sa.LargeBinary(300), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.TIMESTAMP, server_default=None, nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    """Rollback users table creation."""
    op.drop_table(USERS_TABLE_NAME)
