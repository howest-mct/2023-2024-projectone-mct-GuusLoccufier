import threading
from datetime import datetime
import time
import json
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from RPi import GPIO

from Classes.Utilities import *
from Classes.MCP3008 import MCP3008
from Classes.PCF8574 import PCF8574
from Classes.Button import Button
from Classes.Buzzer import Buzzer
from Classes.Encoder import Encoder
from Classes.OLEDDisplay import OLEDDisplay
from Classes.SevenSegmentDisplay import SevenSegmentDisplay

MCP = MCP3008(0, 0)
OLED = OLEDDisplay()
encoder = Encoder(clk=24, dt=23, sw=25)

# Constants
PIEZO_THRESHOLD = 50 # Threshold where a hit is counted
DEBOUNCE_DELAY_MS = 200  # Debounce delay in milliseconds
NUM_CHANNELS = 8  # Number of channels 1 per target

# Globals 
last_event_time = [0] * NUM_CHANNELS # Last time an event was registered for each channel
running_session = None # Current running session

# Flask variables
app = Flask(__name__)
app.config['SECRET_KEY'] = 'loccuF13r'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

def history_add(device, action, json):
    global running_session
    DataRepository.create_event(device, action, json, running_session)
    history = DataRepository.read_history()
    history = convert_to_iso(history)
    socketio.emit('B2F_history', {'history': history})

def convert_to_iso(data):
    for record in data:
        if isinstance(record['timestamp'], datetime):
            record['timestamp'] = record['timestamp'].isoformat()
    return data

def target():
    global last_event_time, running_session
    while True:
        current_time = time.time() * 1000  # Get current time in milliseconds
        for channel in range(NUM_CHANNELS):
            piezoelectric = MCP.read_channel(channel)
            if piezoelectric > PIEZO_THRESHOLD and (current_time - last_event_time[channel]) > DEBOUNCE_DELAY_MS:
                print(f"Piezo Channel {channel} => {piezoelectric}")
                DataRepository.create_event(channel + 1, 1, json.dumps({"value": piezoelectric}), running_session)
                last_event_time[channel] = current_time

                history = DataRepository.read_history()
                history = convert_to_iso(history)
                socketio.emit('B2F_history', {'history': history})
        time.sleep(0.01)  # Small delay to prevent CPU overuse

def control():
    global running_session
    display = "Interface: address"
    for interface, ip in get_ips():
        display += f"\n{interface}: {ip}"
    OLED.clear_display()
    OLED.write_text(display)
    history_add(22, 8, json.dumps({"text": display}))
    
    while True:
        if encoder.pressed():
            print("Encoder pressed")
            history_add(19, 7, None)
            if running_session:
                DataRepository.stop_session(running_session)
                print(f"Session {running_session} stopped")
                running_session = None
            else:
                running_session = DataRepository.start_session(1, 1)
                print(f"Session {running_session} started")
                
        rotation_value = encoder.value()
        if rotation_value != 0:
            print(f"Rotation value: {rotation_value}")
            history_add(19, 6, json.dumps({"rotation": rotation_value}))
        time.sleep(0.01)  # Small delay to prevent CPU overuse

def start_target_thread():
    target_thread = threading.Thread(target=target, daemon=True)
    target_thread.start()
    print("target_thread started")

def start_control_thread():
    control_thread = threading.Thread(target=control, daemon=True)
    control_thread.start()
    print("control_thread started")

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    history = DataRepository.read_history()
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

def cleanup():
    MCP.close()
    OLED.close()

if __name__ == '__main__':
    try:
        start_target_thread()
        start_control_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
        cleanup()
    finally:
        print("finished")
