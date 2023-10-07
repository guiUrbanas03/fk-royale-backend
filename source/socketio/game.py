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

    def add_player(self, player: Player):
        self.players[player.socket_id] = player

        self.notify_all({"type": "add_player", "data": player.resource})

    def add_game(self, game: Game, room: Room, owner_id: str):
        self.games[game.str_id] = game
        self.rooms[room.str_id] = room

        owner: Player = self.get_player(owner_id)
        owner.current_game_id = game.str_id

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
        removed_players: list[Player] = []

        self.games.pop(game.str_id)

        for player_id in room.player_ids:
            player: Player = self.get_player(player_id)
            player.current_game_id = None
            removed_players.append(player.resource)

        self.rooms.pop(room_id)

        self.notify_all(
            {
                "type": "remove_game",
                "data": {"game": game.resource, "room": room.resource, "players": removed_players},
            }
        )

    def add_player_to_room(self, game: Game, player_id: str):
        room: Room = self.get_room(str(game.room_id))
        player: Player = self.get_player(player_id)

        room.player_ids.append(player.socket_id)
        player.current_game_id = game.str_id

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

        self.notify_all(
            {
                "type": "remove_player_from_room",
                "data": {"player": player.resource, "game": game.resource, "room": room.resource},
            }
        )
