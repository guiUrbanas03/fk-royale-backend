from flask import request
from flask_socketio import Namespace, join_room
from uuid import uuid4

from source.models.game_room.game_room import GameRoom


class GameRoomSocket(Namespace):
    def on_connect(self):
        print(f"Client connected to {self.namespace}: {request.sid}")

    def on_disconnect(self):
        print(f"Client disconnected from {self.namespace}: {request.sid}")

    def on_create_game_room(self, data):
        print(f"[{self.namespace}]: {request.sid} joined the room [{data['name']}]")
        game_room = GameRoom(
            str(uuid4()),
            data["player_id"],
            data["name"],
            data["max_players"],
            data["hearts"],
            data["turn_time_seconds"],
            data.get("password"),
        )

        join_room(game_room.id)

        data = {
            "id": game_room.id,
            "player_id": game_room.player_id,
            "name": game_room.name,
            "password": game_room.password,
            "max_players": game_room.max_players,
            "hearts": game_room.hearts,
            "turn_time_seconds": game_room.turn_time_seconds,
        }

        self.emit("create_game_room", data, room=game_room.id)

    def on_leave_game_room(self, data):
        print(f"[{self.namespace}]: {request.sid} left the room {data['id']}")
        self.emit("leave_game_room", data, room=data["id"])
