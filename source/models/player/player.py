from __future__ import annotations

from typing import TYPE_CHECKING

from source.dtos.socketio import PlayerResourceDTO

if TYPE_CHECKING:
    from source.models.game.game import Game
    from source.models.user.user import User


class Player:
    """Define player model."""

    def __init__(self, socket_id: str, user: User) -> None:
        self.socket_id: str = socket_id
        self.user: User = user
        self.current_game: Game = None
        self.status: str = "idle"  # idle | unready | ready | playing

    def __repr__(self) -> str:
        return f"Player({self.socket_id}, {self.user.profile.nickname}, {self.status})"

    @property
    def resource(self):
        return PlayerResourceDTO().dump(self)
