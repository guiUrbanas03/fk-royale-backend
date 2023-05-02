"""Create xp_event_types table.

Revision ID: aa93c9560473
Revises: ccaeaba3e967
Create Date: 2023-02-06 10:50:35.730655
"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import XP_EVENT_TYPES_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "aa93c9560473"
down_revision = "ccaeaba3e967"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create xp_event_types table structure."""
    op.create_table(
        XP_EVENT_TYPES_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("event_name", sa.String(300), unique=True, nullable=False),
        sa.Column("xp_amount", sa.Integer, nullable=False),
        sa.Column("message", sa.String(300), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_name"),
    )


def downgrade() -> None:
    """Rollback xp_event_types table creation."""
    op.drop_table(XP_EVENT_TYPES_TABLE_NAME)
