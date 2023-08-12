"""Store user profile info."""
from sqlalchemy.dialects.postgresql import UUID

from source.constants.tables import PROFILES_TABLE_NAME
from source.database.instance import db
from source.models.columns import created_at, deleted_at, generate_uuid, updated_at


class Profile(db.Model):
    """Define Profile model."""

    __tablename__ = PROFILES_TABLE_NAME

    id = generate_uuid()
    full_name = db.Column(db.String(300), nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    avatar_url = db.Column(db.String(300), nullable=True)
    created_at = created_at()
    updated_at = updated_at()
    deleted_at = deleted_at()

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), unique=True, nullable=False)
    user = db.relationship("User", uselist=False, back_populates="profile")
    game_stats = db.relationship("GameStats", uselist=False, back_populates="profile")
