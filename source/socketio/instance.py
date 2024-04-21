from flask import abort, request
from flask_socketio import SocketIO, close_room, emit, join_room, leave_room
from jwt.exceptions import DecodeError, ExpiredSignatureError

from source.blueprints.auth.services import get_user_by_token
from source.errors.json_error import CauseTypeError, jwt_error
from source.jwt.jwt_causes import JwtCause
from source.models.game.game import Game, GameSettings
from source.models.player.player import Player
from source.models.room.room import Room
from source.models.user.user import User
from source.socketio.game import GameContextManager

socketio: SocketIO = SocketIO(cors_allowed_origins="*", logger=True, async_mode="gevent")
context: GameContextManager = GameContextManager()


def resource(data: dict):
    return data.resource if "resource" in data else data


def socket_command(command: dict):
    print(f"({request.sid})---> Emitting command: {command['type']}, {command['data']}\n")
    if "room" in command:
        emit(command["type"], command["data"], room=command["room"])
    else:
        socketio.emit(command["type"], command["data"])


context.observe(socket_command)


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

    except ExpiredSignatureError as error:
        print("---> EXPIRED ERRROR: ", error["jwt_data"])
        if error["jwt_data"]["type"] == "refresh":
            return jwt_error(JwtCause.REFRESH_TOKEN_EXPIRED.value)
        return jwt_error(JwtCause.ACCESS_TOKEN_EXPIRED.value)


@socketio.on("disconnect")
def disconnect():
    """Disconnect player"""
    try:
        player: Player = context.get_player(request.sid)

        if player.current_game_id:
            leave_game_room({"game_id": player.current_game_id})
        context.remove_player(player)
    except KeyError as error:
        abort(400, {"type": CauseTypeError.DATA_VIOLATION_ERROR.value, "data": str(error)})


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


@socketio.on("get_ready")
def get_ready():
    print(f"{request.sid} is ready to play")
    context.get_ready(request.sid)


@socketio.on("get_unready")
def get_unready():
    print(f"{request.sid} is not ready to play")
    context.get_unready(request.sid)


@socketio.on("start_game_match")
def start_game_match(data):
    print(f"{request.sid}: Starting game match {data}")
    context.start_game_match(data)
