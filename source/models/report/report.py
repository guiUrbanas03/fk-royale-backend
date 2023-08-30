"""Store reports info."""
from sqlalchemy.dialects.postgresql import UUID

from source.constants.tables import REPORTS_TABLE_NAME
from source.database.instance import db
from source.models.columns import created_at, generate_uuid, updated_at


class Report(db.Model):

    __tablename__ = REPORTS_TABLE_NAME

    id = generate_uuid()
    category = db.Column(db.String(300))
    subject = db.Column(db.String(300))
    description = db.Column(db.String(999))
    created_at = created_at()
    updated_at = updated_at()
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey("profiles.id"), nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="reports")
