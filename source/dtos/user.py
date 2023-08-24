"""Define DTOs for user operations."""
import marshmallow as ma
from marshmallow import validate


class CreateUserDTO(ma.Schema):
    """Create user DTO schema."""

    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)


class UserResourceDTO(ma.Schema):
    """User resource DTO schema."""

    id = ma.fields.UUID(required=True)
    email = ma.fields.Email(required=True)


class UserChangePasswordDTO(ma.Schema):
    """User resource change password DTO schema."""

    old_password = ma.fields.Str(required=True)
    new_password = ma.fields.Str(required=True, validate=validate.Length(min=6))
    confirm_new_password = ma.fields.Str(required=True, validate=validate.Length(min=6))


class UserDeleteDTO(ma.Schema):
    """User confirmation to delete account"""

    confirm_deletion = ma.fields.Str(required=True)