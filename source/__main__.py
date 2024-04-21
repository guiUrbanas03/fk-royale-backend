from source import create_app
from source.socketio.instance import socketio

if __name__ == "__main__":
    app = create_app()
    print("running server with socketio")
    socketio.run(app, host="0.0.0.0", port=8000, debug=True, log_output=True, use_reloader=True)
