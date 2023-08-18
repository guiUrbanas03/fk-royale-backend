from flask import request
from flask_socketio import Namespace, join_room, send, emit
from uuid import uuid4
import logging

from source.models.game_room.game_room import GameRoom

class GameRoomSocket(Namespace):
    def on_connect(self):
        print(f"Client connected to {self.namespace}: {request.sid}")

    def on_disconnect(self):
        print(f"Client disconnected from {self.namespace}: {request.sid}")

    def on_create_game_room(self, data):
        game_room = GameRoom(
            uuid4(), 
            data['player_id'], 
            data['name'], 
            data['max_players'], 
            data['hearts'], 
            data['turn_time_seconds'], 
            data.get("password")
        )
        
        join_room(game_room.id)

        data = {
            "id": str(game_room.id),
            "player_id": game_room.player_id,
            "name": game_room.name,
            "password": game_room.password,
            "max_players": game_room.max_players,
            "hearts": game_room.hearts,
            "turn_time_seconds": game_room.turn_time_seconds
        }
        
        emit('create_game_room', data, to=game_room.id)

