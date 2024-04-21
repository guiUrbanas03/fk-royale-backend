from uuid import UUID, uuid4

from source.dtos.socketio import GameResourceDTO, GameSettingsResourceDTO


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

    def __init__(self, room_id: UUID, settings: GameSettings) -> None:
        self.id = uuid4()
        self.status = "waiting"  # waiting | playing | "finished"
        self.room_id: UUID = room_id
        self.settings = settings

    def __repr__(self) -> str:
        return f"{self.str_id}, {self.room_id}, {self.status}"

    @property
    def str_id(self) -> str:
        return str(self.id)

    @property
    def resource(self):
        return GameResourceDTO().dump(self)
