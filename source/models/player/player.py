from __future__ import annotations

from typing import TYPE_CHECKING

from source.dtos.socketio import PlayerResourceDTO

if TYPE_CHECKING:
    from uuid import UUID

    from source.models.user.user import User


class Player:
    """Define player model."""

    def __init__(self, socket_id: str, user: User) -> None:
        self.socket_id: str = socket_id
        self.user: User = user
        self.current_game_id: UUID = None
        self.status: str = "idle"  # idle | unready | ready | playing

    def __repr__(self) -> str:
        return f"Player({self.socket_id}, {self.user.profile.nickname}, {self.status})"

    @property
    def resource(self):
        return PlayerResourceDTO().dump(
            {
                "socket_id": self.socket_id,
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "profile": self.user.profile,
                    "game_stats": self.user.profile.game_stats,
                },
                "current_game_id": self.current_game_id,
                "status": "self.status",
            }
        )
