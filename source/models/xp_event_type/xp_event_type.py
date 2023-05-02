"""Types of xp events to level up."""
from enum import Enum
from typing import Final

from source.constants.tables import XP_EVENT_TYPES_TABLE_NAME
from source.database.instance import db
from source.models.columns import created_at, generate_uuid, updated_at


class XpEventType(db.Model):
    """Define XP Event Type model."""

    __tablename__ = XP_EVENT_TYPES_TABLE_NAME

    id = generate_uuid()
    event_name = db.Column(db.String(300), unique=True, nullable=False)
    xp_amount = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(300), nullable=False)
    created_at = created_at()
    updated_at = updated_at()


class XpEventTypeName(Enum):
    """Enum for xp event type names."""

    WIN_MATCH: Final[str] = "WIN_MATCH"
    WIN_ROUND: Final[str] = "WIN_ROUND"
    WIN_TURN: Final[str] = "WIN_TURN"
    FINISH_MATCH: Final[str] = "FINISH_MATCH"
    FINISH_ROUND: Final[str] = "FINISH_ROUND"
