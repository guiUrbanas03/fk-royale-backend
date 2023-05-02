"""Store revoked token info."""
from sqlalchemy.dialects.postgresql import UUID

from source.constants.tables import REVOKED_TOKENS_TABLE_NAME
from source.database.instance import db
from source.models.columns import created_at, deleted_at, generate_uuid, updated_at


class RevokedToken(db.Model):
    """Define Revoked Token model."""

    __tablename__ = REVOKED_TOKENS_TABLE_NAME

    id = generate_uuid()
    token = db.Column(db.String(), nullable=False)
    type_ = db.Column(db.String(300), nullable=False)
    created_at = created_at()
    updated_at = updated_at()
    deleted_at = deleted_at()

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="revoked_token")
