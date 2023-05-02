"""Track user's game stats."""
from sqlalchemy.dialects.postgresql import UUID

from source.constants.tables import GAME_STATS_TABLE_NAME
from source.database.instance import db
from source.models.columns import created_at, deleted_at, generate_uuid, updated_at


class GameStats(db.Model):
    """Define GameStats model."""

    __tablename__ = GAME_STATS_TABLE_NAME

    id = generate_uuid()
    level = db.Column(db.Integer, server_default="0", nullable=False)
    matches = db.Column(db.Integer, server_default="0", nullable=False)
    victories = db.Column(db.Integer, server_default="0", nullable=False)
    xp_points = db.Column(db.Integer, server_default="0", nullable=False)
    created_at = created_at()
    updated_at = updated_at()
    deleted_at = deleted_at()

    profile_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("profiles.id"), unique=True, nullable=False
    )

    profile = db.relationship("Profile", backref="game_stats")
