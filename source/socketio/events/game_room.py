from flask import abort, request
from flask_socketio import Namespace, join_room, leave_room
from jwt.exceptions import DecodeError

from source.blueprints.auth.services import get_user_by_token
from source.dtos.socketio import SocketStateResourceDTO
from source.errors.json_error import CauseTypeError
from source.models.game.game import Game, GameSettings
from source.models.player.player import Player
from source.models.room.room import Room
from source.models.user.user import User


class SocketState:
    """Define socket state."""

    def __init__(self) -> None:
        self.games: list[Game] = []
        self.players: list[Player] = []
        self.current_player: Player = None

    def __repr__(self) -> str:
        return f"SocketState({self.games}, {self.players}, {self.current_player}, {self.games})"

    def get_game(self, id: str) -> Room:
        return next(filter(lambda game: game.str_id == id, self.games))

    @property
    def resource(self):
        return SocketStateResourceDTO().dump(self)


class GameRoomSocket(Namespace):
    """Handle socket events."""

    state: SocketState = SocketState()

    def on_connect(self, data):
        """On connect event"""
        try:
            print("---> CONNECT: ", request.sid)
            user: User = get_user_by_token(data["token"])
            player: Player = Player(request.sid, user)
            self.state.players.append(player)
            self.state.current_player = player

            self.emit("fetch_state", self.state.resource)
            print("---->: ", self.state)
            print("----> state resource: ", self.state.resource)

        except DecodeError as error:
            abort(401, {"type": CauseTypeError.TOKEN_ERROR.value, "data": str(error)})

    def on_disconnect(self):
        print("---> DISCONNECT: ", self.state.current_player)
        self.state.players.remove(self.state.current_player)

    def on_create_game_room(self, data):
        print("---> CREATE ROOM: ", self.state.current_player)

        room: Room = Room(
            name=data["name"],
            password=data["password"],
            owner=self.state.current_player,
        )

        settings: GameSettings = GameSettings(
            max_players=data["max_players"],
            lives=data["lives"],
            turn_time_seconds=data["turn_time_seconds"],
        )

        game: Game = Game(room, settings)

        self.state.games.append(game)
        self.state.current_player.current_game = game

        join_room(room.str_id)

        self.emit("create_game_room", game.resource, room=room.str_id)
        self.emit("fetch_state", self.state.resource)

    def on_join_game_room(self, data):
        print(f"[{self.namespace}]: {request.sid} joined the room [{data['room']['name']}]")
        game: Game = self.state.get_game(data["id"])
        game.room.players.append(self.state.current_player)
        self.state.current_player.current_game = game
        join_room(game.room.str_id)

        self.emit("join_game_room", game.resource, room=game.room.str_id)
        self.emit("fetch_state", self.state.resource)

    def on_leave_game_room(self, data):
        print(f"[{self.namespace}]: {request.sid} left the room {data['room']['id']}")
        game: Game = self.state.current_player.current_game
        game.room.players.remove(self.state.current_player)

        self.state.current_player.current_game = None

        self.emit("leave_game_room", game.resource, room=game.room.str_id)
        leave_room(game.room.str_id)

        if len(game.room.players) == 0:
            self.close_room(game.room.str_id)
            self.state.games.remove(game)

        self.emit("fetch_state", self.state.resource)
