from uuid import uuid4

from source.dtos.socketio import RoomResourceDTO
from source.models.player.player import Player


class Room:
    """Define room model."""

    def __init__(self, name: str, password: str, owner: Player) -> None:
        self.id = uuid4()
        self.name = name
        self.password = password
        self.owner = owner
        self.players: list[Player] = [self.owner]

    def __repr__(self) -> str:
        return f"Room({self.str_id}, {self.name}, {self.owner})"

    @property
    def str_id(self):
        return str(self.id)

    @property
    def resource(self):
        return RoomResourceDTO().dump(self)
