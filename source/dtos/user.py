"""Define DTOs for user operations."""
import marshmallow as ma


class CreateUserDTO(ma.Schema):
    """Create user DTO schema."""

    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)


class UserResourceDTO(ma.Schema):
    """User resource DTO schema."""

    id = ma.fields.UUID(required=True)
    email = ma.fields.Email(required=True)
