from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
from datetime import datetime, timedelta

diff = 0

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update-diff', methods=['POST'])
def update_diff():
    ip_address = request.remote_addr
    global diff
    request_data = request.get_json()
    new_diff = request_data.get("difference")
    sendlog('POST /update-diff data: ' + str(new_diff), ip_address)
    if new_diff is not None:
        try:
            diff = int(new_diff)
            sendlog('Difference updated, returning ok. ' + 'new difference= ' + str(new_diff), ip_address)
            return 'OK'
        except ValueError:
            sendlog('Invalid value for difference, returning 400. ' + 'difference = ' + str(new_diff), ip_address)
            return 'Invalid value for diff', 400
    else:
        sendlog('No difference provided, returning 400. ', ip_address)
        return 'No diff provided', 400

@app.route('/getdiff', methods=['GET'])
def getdiff():
    ip_address = request.remote_addr
    request_data = request.get_json()
    new_time = request_data.get("date")
    sendlog('GET /getdiff data: ' + str(new_time), ip_address)
    if new_time is not None:
        try:
            hosttime = datetime.fromisoformat(new_time).replace(tzinfo=None)
            mytime = datetime.now().replace(tzinfo=None)
            mydiff = (hosttime-mytime).total_seconds()*1000
            sendlog('difference obtained, returning ok. ' + 'difference= ' + str(mydiff), ip_address)
            return jsonify({'difference': mydiff}), 200
        except ValueError:
            sendlog('Invalid value for date, returning 400. ', ip_address)
            return 'Invalid value for date, expected in iso 8601', 400
    else:
        sendlog('No date provided, returning 400. ', ip_address)
        return 'No date provided', 400

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

def sendlog(msg, ip):
    thetime = datetime.now()
    socketio.emit('log', '['+ thetime.strftime('%m/%d/%y %H:%M:%S') + '] ' + msg + ' ip: ' + ip)
    

if __name__ == '__main__':
    socketio.run(app)