"""Define DTOs for game stats operations."""
import marshmallow as ma


class CreateGameStatsDTO(ma.Schema):
    """Create game stats DTO schema."""

    profile_id = ma.fields.UUID(required=True)


class GameStatsResourceDTO(ma.Schema):
    """game stats resource DTO schema."""

    id = ma.fields.UUID(required=True)
    profile_id = ma.fields.UUID(required=True)
    level = ma.fields.Integer(required=True)
    matches = ma.fields.Integer(required=True)
    victories = ma.fields.Integer(required=True)
    xp_points = ma.fields.Integer(required=True)
