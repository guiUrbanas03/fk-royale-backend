"""report_bug

Revision ID: 1525890b9bd9
Revises: f9a150afc985
Create Date: 2023-08-28 13:52:52.986703

"""
import sqlalchemy as sa
from alembic import op
from uuid import uuid4

from source.constants.tables import REPORTS_TABLE_NAME

# revision identifiers, used by Alembic.
revision = "1525890b9bd9"
down_revision = "f9a150afc985"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        REPORTS_TABLE_NAME,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, server_default=str(uuid4())),
        sa.Column("category", sa.String(300), nullable=False),
        sa.Column("subject", sa.String(300), nullable=False),
        sa.Column("description", sa.String(999), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            onupdate=sa.text("now()"),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("profile_id", sa.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"]),
    )


def downgrade() -> None:
    op.drop_table(REPORTS_TABLE_NAME)
