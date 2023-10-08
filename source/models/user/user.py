"""Store user auth data."""

from source.constants.tables import USERS_TABLE_NAME
from source.database.instance import db
from source.dtos.user import FullUserResourceDTO, UserResourceDTO
from source.models.columns import created_at, deleted_at, generate_uuid, updated_at


class User(db.Model):
    """Define User model."""

    __tablename__ = USERS_TABLE_NAME

    id = generate_uuid()
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(300), nullable=False)
    created_at = created_at()
    updated_at = updated_at()
    deleted_at = deleted_at()
    profile = db.relationship("Profile", uselist=False, back_populates="user")

    def __repr__(self) -> str:
        return f"User({self.id}, {self.email}, {self.created_at})"

    @property
    def resource(self):
        return UserResourceDTO().dump(self)

    @property
    def full_resource(self):
        return FullUserResourceDTO().dump(
            {**self, "profile": self.profile, "game_stats": self.profile.game_stats}
        )
