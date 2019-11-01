from flask_socketio import SocketIO, disconnect, send
from threading import Lock

thread = None
async_mode = None
socketio = SocketIO()
thread_lock = Lock()


@socketio.on('connect')
def on_connect():
    print('Connect...')


@socketio.on('disconnect')
def on_disconnect():
    print('Disconnect')
    disconnect()


@socketio.on('message')
def handle_message(msg):
    print('Message', msg)
    send(msg, broadcast=True)