from flask_socketio import SocketIO
from source.socketio.events.game_room import GameRoomSocket
from source.constants.socketio import GAME_ROOM_NAMESPACE

socketio: SocketIO = SocketIO(cors_allowed_origins="*", logger=True)
socketio.on_namespace(GameRoomSocket("/game-room"))
import source.socketio.events.index