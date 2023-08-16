class GameRoom:
    def __init__(self, id, player_id, name, settings, password=None) -> None:
        self.id = id
        self.player_id = player_id
        self.name = name
        self.settings = settings
        self.password = password


class GameRoomSettings:
    def __init__(self, max_players=8, hearts=3, turn_time_seconds=30) -> None:
        self.max_players = max_players
        self.hearts = hearts
        self.turn_time_seconds = turn_time_seconds

