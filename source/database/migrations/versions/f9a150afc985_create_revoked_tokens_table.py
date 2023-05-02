"""create revoked_tokens table

Revision ID: f9a150afc985
Revises: aa93c9560473
Create Date: 2023-04-23 16:16:15.754294

"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import REVOKED_TOKENS_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "f9a150afc985"
down_revision = "aa93c9560473"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create revoked tokens table structure."""
    op.create_table(
        REVOKED_TOKENS_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("type_", sa.String(300), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.TIMESTAMP, server_default=None, nullable=True),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    """Rollback revoked tokens table creation."""
    op.drop_table(REVOKED_TOKENS_TABLE_NAME)
