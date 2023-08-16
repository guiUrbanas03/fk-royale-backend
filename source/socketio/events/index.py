from source.socketio.instance import socketio


@socketio.on('connect')
def on_connect():
    print('[SOCKET]: user connected')