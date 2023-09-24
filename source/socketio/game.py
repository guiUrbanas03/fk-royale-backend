from flask import request

from source.dtos.socketio import GameAndPlayerResourceDTO, GameContextResourceDTO
from source.models.game.game import Game
from source.models.player.player import Player
from source.models.room.room import Room
from source.patterns.observer.observer import Observer


class GameAndPlayer:
    def __init__(self, game: Game, player: Player) -> None:
        self.game = game
        self.player = player

    @property
    def resource(self):
        return GameAndPlayerResourceDTO().dump({"game": self.game, "player": self.player})


class GameContextManager(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.games: dict[str, Game] = {}
        self.players: dict[str, Player] = {}

    @property
    def resource(self):
        return GameContextResourceDTO().dump({"games": self.games, "players": self.players})

    def get_game(self, id: str) -> Game:
        return self.games[id]

    def get_player(self, id: str) -> Player:
        return self.players[id]

    def add_player(self, player: Player):
        self.players[player.socket_id] = player

        self.notify_all({"type": "add_player", "data": player})

    def remove_player(self, player: Player):
        self.players.pop(player.socket_id)

        self.notify_all({"type": "remove_player", "data": player})

    def add_game(self, game: Game):
        self.games[game.str_id] = game

        self.players[request.sid].current_game = game

        self.notify_all({"type": "add_game", "data": game})

    def remove_game(self, game: Game):
        self.games.pop(game.str_id)

        self.players[request.sid].current_game = None

        self.notify_all({"type": "remove_game", "data": game})

    def add_to_room(self, game: Game, player: Player):
        room: Room = self.games[game.str_id].room

        room.players.append(player)
        player.current_game = game

        self.notify_all({"type": "add_to_room", "data": GameAndPlayer(game, player)})

    def remove_from_room(self, game: Game, player: Player):
        room: Room = self.games[game.str_id].room

        room.players.remove(player)
        player.current_game = None

        self.notify_all({"type": "remove_from_room", "data": GameAndPlayer(game, player)})
