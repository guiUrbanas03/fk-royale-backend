from flask import request
from source.socketio.instance import socketio


@socketio.on('connect')
def on_connect():
    print(f"Client connected to socket: {request.sid}")


@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected from socket: {request.sid}")