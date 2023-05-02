"""Define DTOs for revoked token operations."""
import marshmallow as ma


class CreateRevokedTokenDTO(ma.Schema):
    """Create revoked token DTO schema."""

    user_id = ma.fields.UUID(required=True)
    token = ma.fields.Str(required=True)
    type_ = ma.fields.Str(required=True)


class RevokedTokenResourceDTO(ma.Schema):
    """Revoked token resource DTO schema."""

    id = ma.fields.UUID(required=True)
    user_id = ma.fields.UUID(required=True)
    token = ma.fields.Str(required=True)
    type_ = ma.fields.Str(required=True)
