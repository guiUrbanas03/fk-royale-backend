from source.socketio.instance import socketio


@socketio.on('connect')
def on_connect():
    print('----------->user connected')


@socketio.on('message')
def on_message(data):
    print('----------->message: ', data)