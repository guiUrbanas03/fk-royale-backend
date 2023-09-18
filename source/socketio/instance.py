from flask import abort, request
from flask_socketio import SocketIO, emit, join_room, leave_room
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


def _command_function(command: dict):
    print(f"({request.sid})---> Emitting command: {command['type']}, {command['data']}\n")
    socketio.emit(command["type"], command["data"].resource)


context.observe(_command_function)


@socketio.on("connect")
def connect(data: dict = {}):
    """Connect new player."""
    try:
        print("--> Player connected: ", request.sid)
        user: User = get_user_by_token(data.get("token"))
        player: Player = Player(request.sid, user)

        context.add_player(player)

        emit("fetch_state", {**context.resource, "current_player": player.resource})

    except DecodeError as error:
        abort(401, {"type": CauseTypeError.TOKEN_ERROR.value, "data": str(error)})


@socketio.on("disconnect")
def disconnect():
    """Disconnect player"""
    player: Player = context.players[request.sid]

    context.remove_player(player)


@socketio.on("create_game_room")
def create_game_room(data):
    room: Room = Room(
        name=data["name"],
        password=data["password"],
        owner=context.players[request.sid],
    )

    settings: GameSettings = GameSettings(
        max_players=data["max_players"],
        lives=data["lives"],
        turn_time_seconds=data["turn_time_seconds"],
    )

    game: Game = Game(room, settings)
    player: Player = context.get_player(request.sid)

    context.add_game(game)

    join_room(room.str_id)

    emit("create_game_room", {"game": game.resource, "player": player.resource}, room=room.str_id)


@socketio.on("join_game_room")
def join_game_room(data):
    print(f"{request.sid} joined the room [{data['room']['name']}]")
    game: Game = context.get_game(data["id"])
    player: Player = context.get_player(request.sid)

    context.add_to_room(game, player)

    join_room(game.room.str_id)

    emit(
        "join_game_room", {"game": game.resource, "player": player.resource}, room=game.room.str_id
    )


@socketio.on("leave_game_room")
def leave_game_room(data):
    print(f"{request.sid} left the room {data['room']['id']}")
    game: Game = context.get_game(data["id"])
    player: Player = context.get_player(request.sid)

    context.remove_from_room(game, player)

    emit(
        "leave_game_room", {"game": game.resource, "player": player.resource}, room=game.room.str_id
    )

    leave_room(game.room.str_id)

    # TODO: Fix remove game when last player leaves.
    # if len(game.room.players) == 0:
    #     close_room(game.room.str_id)
    #     context.remove_game(game)
