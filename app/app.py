from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from datetime import datetime, timedelta

diff = 0

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('start_stream')
def start_stream():
    print('Starting stream')
    while True:
        delta = timedelta(milliseconds=diff)
        hora_actual = datetime.now()
        nueva_hora = hora_actual + delta
        socketio.emit('update-time', nueva_hora.strftime('%H:%M:%S'))
        time.sleep(1)

if __name__ == '__main__':
    socketio.run(app)