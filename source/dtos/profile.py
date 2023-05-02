"""Define DTOs for profile operations."""
import marshmallow as ma


class CreateProfileDTO(ma.Schema):
    """Create profile DTO schema."""

    full_name = ma.fields.Str(required=True)
    nickname = ma.fields.Str(required=True)
    user_id = ma.fields.UUID(required=True)


class ProfileResourceDTO(ma.Schema):
    """Profile resource DTO schema."""

    id = ma.fields.UUID(required=True)
    user_id = ma.fields.UUID(required=True)
    full_name = ma.fields.Str(required=True)
    nickname = ma.fields.Str(required=True)
    avatar_url = ma.fields.Str()
