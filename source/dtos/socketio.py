import marshmallow as ma

from source.dtos.user import UserResourceDTO


class PlayerResourceDTO(ma.Schema):
    """Player resource dto."""

    socket_id = ma.fields.Str(required=True)
    user = ma.fields.Nested(UserResourceDTO)
    current_game = ma.fields.Nested(lambda: GameResourceDTO())
    status = ma.fields.Str(required=True)


class RoomResourceDTO(ma.Schema):
    """Room resource dto."""

    id = ma.fields.UUID(required=True)
    name = ma.fields.Str(required=True)
    password = ma.fields.Str()
    owner = ma.fields.Nested(PlayerResourceDTO(exclude=["current_game"]))
    players = ma.fields.Nested(PlayerResourceDTO(exclude=["current_game"]), many=True)


class GameSettingsResourceDTO(ma.Schema):
    """Game settings resource dto."""

    max_players = ma.fields.Integer(required=True)
    lives = ma.fields.Integer(required=True)
    turn_time_seconds = ma.fields.Integer(required=True)


class GameResourceDTO(ma.Schema):
    """Game resource dto."""

    id = ma.fields.UUID(required=True)
    status = ma.fields.Str(required=True)
    room = ma.fields.Nested(RoomResourceDTO)
    settings = ma.fields.Nested(GameSettingsResourceDTO)


class SocketStateResourceDTO(ma.Schema):
    """Socket state resource dto."""

    games = ma.fields.Nested(GameResourceDTO, many=True)
    players = ma.fields.Nested(PlayerResourceDTO, many=True)
    current_player = ma.fields.Nested(PlayerResourceDTO)
