import threading
from datetime import datetime
import time
import json
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from RPi import GPIO

from Classes.MCP3008 import MCP3008

MCP = MCP3008(0, 0)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'loccuF13r'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

def convert_to_iso(data):
    for record in data:
        if isinstance(record['timestamp'], datetime):
            record['timestamp'] = record['timestamp'].isoformat()
    return data

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def mcp():
    MCP = MCP3008(0, 0)
    while True:
        # TODO: Add all piezo's and a debounce with millis
        piezoelectric = MCP.read_channel(0x00)
        if piezoelectric > 50:
            print(f"Piezzo => {piezoelectric}")
            nieuw_type = DataRepository.create_event(1, 1, json.dumps({"value": piezoelectric}), None)
            history = DataRepository.read_history()
            history = convert_to_iso(history)
            socketio.emit('B2F_history', {'history': history})

def start_mcp_thread():
    mcp_thread = threading.Thread(target=mcp, daemon=True)
    mcp_thread.start()
    print("mcp_thread started")

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    history = DataRepository.read_history()
    # Beter is het om enkel naar de client te sturen die de verbinding heeft gemaakt.
    history = convert_to_iso(history)
    emit('B2F_history', {'history': history}, broadcast=False)


# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     print('licht gaat aan/uit', data)
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     # spreek de hardware aan
#     # stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)
#     print(res)
#     # vraag de (nieuwe) status op van de lamp
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp',  {'lamp': data})
#     # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#     if lamp_id == '3':
#         print(f"TV kamer moet switchen naar {new_status} !")
#         # Do something


if __name__ == '__main__':
    try:
        start_mcp_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
        MCP.close()
    finally:
        print("finished")
