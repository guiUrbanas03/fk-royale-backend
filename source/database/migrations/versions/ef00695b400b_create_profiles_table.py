"""Create profiles table.

Revision ID: ef00695b400b
Revises: 8d2fffd52f76
Create Date: 2023-02-06 10:37:09.583566
"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import PROFILES_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "ef00695b400b"
down_revision = "8d2fffd52f76"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create profiles table structure."""
    op.create_table(
        PROFILES_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("full_name", sa.String(300), nullable=False),
        sa.Column("nickname", sa.String(20), unique=True, nullable=False),
        sa.Column("avatar_url", sa.String(300), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.TIMESTAMP, server_default=None, nullable=True),
        sa.Column("user_id", sa.UUID(as_uuid=True), unique=True, nullable=False),
        sa.UniqueConstraint("nickname"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    """Rollback profiles table creation."""
    op.drop_table(PROFILES_TABLE_NAME)
