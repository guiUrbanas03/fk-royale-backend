# class GameRoomModel(db.Model):
#     """Define GameStats model."""

#     __tablename__ = GAME_ROOM_TABLE_NAME

#     id = generate_uuid()
#     name = db.Column(db.String)
#     password = db.Column(db.String)
#     max_players = db.Column(db.Integer)
#     lives = db.Column(db.Integer)
#     turn_time_seconds = db.Column(db.Integer)
#     created_at = created_at()
#     updated_at = updated_at()

#     user_id = db.Column(
#         UUID(as_uuid=True), db.ForeignKey("users.id"), unique=True, nullable=False
#     )

#     user = db.relationship("User", uselist=False, back_populates="game_room")


class GameRoom:
    def __init__(
        self,
        id: str,
        player_id: str,
        name: str,
        max_players: int,
        hearts: int,
        turn_time_seconds: int,
        password: str = None,
    ) -> None:
        self.id = id
        self.player_id = player_id
        self.name = name
        self.password = password
        self.max_players = max_players
        self.hearts = hearts
        self.turn_time_seconds = turn_time_seconds
