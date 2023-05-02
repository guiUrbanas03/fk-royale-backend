"""Define DTOs for auth operations."""
import marshmallow as ma


class LoginUserDTO(ma.Schema):
    """Login user DTO schema."""

    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)
