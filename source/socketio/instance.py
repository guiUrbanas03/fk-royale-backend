from flask import abort, request
from flask_socketio import SocketIO, close_room, emit, join_room, leave_room
from jwt.exceptions import DecodeError

from source.blueprints.auth.services import get_user_by_token
from source.errors.json_error import CauseTypeError
from source.models.game.game import Game, GameSettings
from source.models.player.player import Player
from source.models.room.room import Room
from source.models.user.user import User
from source.socketio.game import GameContextManager

socketio: SocketIO = SocketIO(cors_allowed_origins="*", logger=True)

context: GameContextManager = GameContextManager()


def resource(data: dict):
    return data.resource if "resource" in data else data


def _command_function(command: dict):
    print(f"({request.sid})---> Emitting command: {command['type']}, {command['data']}\n")
    socketio.emit(command["type"], command["data"])


context.observe(_command_function)


@socketio.on("connect")
def connect(data: dict = {}):
    """Connect new player."""
    try:
        if data:
            user: User = get_user_by_token(data.get("token"))
            player: Player = Player(request.sid, user)

            context.add_player(player)
            emit("fetch_state", context.resource)

    except DecodeError as error:
        abort(401, {"type": CauseTypeError.TOKEN_ERROR.value, "data": str(error)})


@socketio.on("disconnect")
def disconnect():
    """Disconnect player"""
    player: Player = context.get_player(request.sid)

    context.remove_player(player)


@socketio.on("create_game_room")
def create_game_room(data):
    room: Room = Room(
        name=data["name"],
        password=data["password"],
        owner_id=context.get_player(request.sid).socket_id,
    )

    settings: GameSettings = GameSettings(
        max_players=data["max_players"],
        lives=data["lives"],
        turn_time_seconds=data["turn_time_seconds"],
    )

    game: Game = Game(room.str_id, settings)

    join_room(room.str_id)

    context.add_game(game, room, request.sid)


@socketio.on("join_game_room")
def join_game_room(data):
    print(f"{request.sid} joined the room {data['game_id']}")
    game: Game = context.get_game(data["game_id"])

    join_room(str(game.room_id))

    context.add_player_to_room(game, request.sid)


@socketio.on("leave_game_room")
def leave_game_room(data):
    print(f"{request.sid} left the room {data['game_id']}")
    game: Game = context.get_game(data["game_id"])
    room_id: str = str(game.room_id)

    leave_room(room_id)

    context.remove_player_from_room(game, request.sid)

    if request.sid == context.get_room(room_id).owner_id:
        close_room(room_id)
        context.remove_game(game)
