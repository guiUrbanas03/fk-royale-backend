"""Create game_stats table.

Revision ID: ccaeaba3e967
Revises: ef00695b400b
Create Date: 2023-02-06 10:37:31.915794
"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import GAME_STATS_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "ccaeaba3e967"
down_revision = "ef00695b400b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create game_stats table structure."""
    op.create_table(
        GAME_STATS_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("level", sa.Integer, server_default="0", nullable=False),
        sa.Column("matches", sa.Integer, server_default="0", nullable=False),
        sa.Column("victories", sa.Integer, server_default="0", nullable=False),
        sa.Column("xp_points", sa.Integer, server_default="0", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.TIMESTAMP, server_default=None, nullable=True),
        sa.Column("profile_id", sa.UUID(as_uuid=True), unique=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"]),
    )


def downgrade() -> None:
    """Rollback game_stats table creation."""
    op.drop_table(GAME_STATS_TABLE_NAME)
