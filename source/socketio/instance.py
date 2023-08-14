from flask_socketio import SocketIO

socketio: SocketIO = SocketIO(cors_allowed_origins="*", logger=True)
import source.socketio.events.index