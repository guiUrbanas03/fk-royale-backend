import marshmallow as ma

from source.dtos.user import FullUserResourceDTO


class PlayerResourceDTO(ma.Schema):
    """Player resource dto."""

    socket_id = ma.fields.Str(required=True)
    user = ma.fields.Nested(FullUserResourceDTO)
    current_game_id = ma.fields.UUID()
    status = ma.fields.Str(required=True)


class RoomResourceDTO(ma.Schema):
    """Room resource dto."""

    id = ma.fields.UUID(required=True)
    name = ma.fields.Str(required=True)
    password = ma.fields.Str()
    owner_id = ma.fields.Str(required=True)
    player_ids = ma.fields.List(ma.fields.Str(), required=True)


class GameSettingsResourceDTO(ma.Schema):
    """Game settings resource dto."""

    max_players = ma.fields.Integer(required=True)
    lives = ma.fields.Integer(required=True)
    turn_time_seconds = ma.fields.Integer(required=True)


class GameResourceDTO(ma.Schema):
    """Game resource dto."""

    id = ma.fields.UUID(required=True)
    status = ma.fields.Str(required=True)
    room_id = ma.fields.UUID(required=True)
    settings = ma.fields.Nested(GameSettingsResourceDTO)


class GameContextResourceDTO(ma.Schema):
    games = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Nested(GameResourceDTO))
    players = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Nested(PlayerResourceDTO))
    rooms = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Nested(RoomResourceDTO))
