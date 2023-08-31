"""Define DTOs for reports operations."""
import marshmallow as ma
from marshmallow import validate


class CreateReportDTO(ma.Schema):
    """Create Report DTO schema."""

    category = ma.fields.Str(required=True, validate=validate.OneOf(["bugs", "suggestions"]))
    subject = ma.fields.Str(required=True, validate=validate.Length(min=3))
    description = ma.fields.Str(required=True, validate=validate.Length(min=3))
    profile_id = ma.fields.UUID(required=True)
