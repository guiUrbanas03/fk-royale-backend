from uuid import uuid4

from source.dtos.socketio import RoomResourceDTO


class Room:
    """Define room model."""

    def __init__(self, name: str, password: str, owner_id: str) -> None:
        self.id = uuid4()
        self.name = name
        self.password = password
        self.owner_id: str = owner_id
        self.player_ids: list[str] = [self.owner_id]

    def __repr__(self) -> str:
        return f"Room({self.str_id}, {self.name}, {self.owner_id})"

    @property
    def str_id(self):
        return str(self.id)

    @property
    def resource(self):
        return RoomResourceDTO().dump(self)
