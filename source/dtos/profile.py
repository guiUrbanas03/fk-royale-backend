"""Define DTOs for profile operations."""
import marshmallow as ma
from marshmallow import validate


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


class UpdateProfileDTO(ma.Schema):
    """Update Profile DTO schema"""

    nickname = ma.fields.Str(required=True, validate=validate.Length(min=3))
    full_name = ma.fields.Str(required=True, validate=validate.Length(min=3))
