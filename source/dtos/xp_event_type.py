"""Define DTOs for XP event types operations."""
import marshmallow as ma

class XpEventTypeResourceDTO(ma.Schema):
    """XP event type resource DTO schema."""
    
    id = ma.fields.UUID(required=True)
    event_name = ma.fields.Str(required=True)
    xp_amount = ma.fields.Integer(required=True)
    message = ma.fields.Str(required=True)

    