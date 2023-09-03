from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from source.dtos.socketio import GameResourceDTO, GameSettingsResourceDTO

if TYPE_CHECKING:
    from source.models.room.room import Room


class GameSettings:
    """Define game settings model."""

    def __init__(self, max_players: int = 8, lives: int = 3, turn_time_seconds: int = 60) -> None:
        self.max_players = max_players
        self.lives = lives
        self.turn_time_seconds = turn_time_seconds

    def __repr__(self) -> str:
        return f"GameSettings({self.max_players}, {self.lives}, {self.turn_time_seconds})"

    @property
    def resource(self):
        return GameSettingsResourceDTO().dump(self)


class Game:
    """Define game model."""

    def __init__(self, room: Room, settings: GameSettings) -> None:
        self.id = uuid4()
        self.status = "waiting"  # waiting | playing
        self.room = room
        self.settings = settings

    def __repr__(self) -> str:
        return f"{self.str_id}, {self.room.name}, {self.status}, {self.room}"

    @property
    def str_id(self) -> str:
        return str(self.id)

    @property
    def resource(self):
        return GameResourceDTO().dump(self)
