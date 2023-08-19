from flask_socketio import SocketIO

from source.socketio.events.game_room import GameRoomSocket

socketio: SocketIO = SocketIO(cors_allowed_origins="*", logger=True)
socketio.on_namespace(GameRoomSocket("/game-room"))
