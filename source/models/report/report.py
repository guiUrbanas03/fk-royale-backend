"""Store reports info."""
from sqlalchemy.dialects.postgresql import UUID
from source.database.instance import db
from source.models.columns import created_at, updated_at, generate_uuid



class Report(db.Model):
   __tablename__ = "reports"
   id = generate_uuid()
   category = db.Column(db.String(300))
   subject = db.Column(db.String(300))
   description = db.Column(db.String(999))
   created_at = created_at()
   updated_at = updated_at()
   profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey("profiles.id"), nullable=False)
   profile = db.relationship("Profile", uselist=False, back_populates="reports")