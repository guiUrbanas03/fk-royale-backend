from source.dtos.socketio import GameContextResourceDTO
from source.models.game.game import Game
from source.models.player.player import Player
from source.models.room.room import Room
from source.patterns.observer.observer import Observer


class GameContextManager(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.players: dict[str, Player] = {}
        self.games: dict[str, Game] = {}
        self.rooms: dict[str, Room] = {}

    @property
    def resource(self):
        return GameContextResourceDTO().dump(
            {"players": self.players, "games": self.games, "rooms": self.rooms}
        )

    def get_player(self, id: str) -> Player:
        return self.players[id]

    def get_game(self, id: str) -> Game:
        return self.games[id]

    def get_room(self, id: str) -> Room:
        return self.rooms[id]

    def get_players_in_room(self, room: Room) -> list[Player]:
        players: list[Player] = []

        for player_id in room.player_ids:
            players.append(self.get_player(player_id))

        return players

    def add_player(self, player: Player):
        self.players[player.socket_id] = player

        self.notify_all({"type": "add_player", "data": player.resource})

    def add_game(self, game: Game, room: Room, owner_id: str):
        self.games[game.str_id] = game
        self.rooms[room.str_id] = room

        owner: Player = self.get_player(owner_id)
        owner.current_game_id = game.str_id
        owner.status = "owner"

        added_room: Room = self.get_room(room.str_id)
        added_room.player_ids = [owner_id]

        self.notify_all(
            {
                "type": "add_game",
                "data": {
                    "player": owner.resource,
                    "game": game.resource,
                    "room": added_room.resource,
                },
            }
        )

    def remove_player(self, player: Player):
        self.players.pop(player.socket_id)

        self.notify_all({"type": "remove_player", "data": player.resource})

    def remove_game(self, game: Game):
        room_id = str(game.room_id)
        room: Room = self.get_room(room_id)
        players = self.get_players_in_room(room)

        self.games.pop(game.str_id)

        for player in players:
            player.current_game_id = None
            player.status = "idle"

        self.rooms.pop(room_id)

        self.notify_all(
            {
                "type": "remove_game",
                "data": {
                    "game": game.resource,
                    "room": room.resource,
                    "players": [player.resource for player in players],
                },
            }
        )

    def add_player_to_room(self, game: Game, player_id: str):
        room: Room = self.get_room(str(game.room_id))
        player: Player = self.get_player(player_id)

        room.player_ids.append(player.socket_id)
        player.current_game_id = game.str_id
        player.status = "unready"

        self.notify_all(
            {
                "type": "add_player_to_room",
                "data": {"player": player.resource, "game": game.resource, "room": room.resource},
            }
        )

    def remove_player_from_room(self, game: Game, player_id: str):
        room: Room = self.get_room(str(game.room_id))
        player: Player = self.get_player(player_id)

        room.player_ids.remove(player_id)
        player.current_game_id = None
        player.status = "idle"

        self.notify_all(
            {
                "type": "remove_player_from_room",
                "data": {"player": player.resource, "game": game.resource, "room": room.resource},
            }
        )

    def get_ready(self, player_id: str):
        player: Player = self.get_player(player_id)
        player.status = "ready"

        self.notify_all(
            {
                "type": "get_ready",
                "data": player.resource,
            }
        )

    def get_unready(self, player_id: str):
        player: Player = self.get_player(player_id)
        player.status = "unready"

        self.notify_all(
            {
                "type": "get_unready",
                "data": player.resource,
            }
        )

    def start_game_match(self, game_id: str):
        game: Game = self.get_game(game_id)
        room: Room = self.get_room(str(game.room_id))
        players: list[Player] = self.get_players_in_room(room)

        game.status = "playing"

        for player in players:
            player.status = "playing"

        self.notify_all(
            {
                "type": "start_game_match",
                "data": {"game": game.resource, "players": [player.resource for player in players]},
            }
        )
