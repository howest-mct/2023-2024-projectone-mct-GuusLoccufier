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
TargetPCF = PCF8574(0x20)
OLED = OLEDDisplay()
encoder = Encoder(clk=24, dt=23, sw=25)
buzzer = Buzzer(12)
b1 = Button(20)
b2 = Button(21)
scoreboard = SevenSegmentDisplay(0x3a)

# Constants
PIEZO_THRESHOLD = 50 # Threshold where a hit is counted
DEBOUNCE_DELAY_MS = 200  # Debounce delay in milliseconds
NUM_CHANNELS = 8  # Number of channels 1 per target

# Globals 
last_event_time = [0] * NUM_CHANNELS # Last time an event was registered for each channel
running_session = None # Current running session
active_user = None
current_course = None
total_hits = 0

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

def send_user():
    global active_user
    if active_user:
        user = DataRepository.get_user(active_user)
        print(f'Sending user {user}')
        socketio.emit('B2F_user', {'user': active_user, 'name': user["username"]})
    else:
        emit('B2F_user', {'user': active_user}, broadcast=False)

def get_encoder_state():
    encoder_value = encoder.value()
    encoder_pressed = encoder.pressed()
    if encoder_pressed:
        print("Encoder pressed")
    if encoder_value != 0:
        print(f"Encoder value: {encoder_value}")
        history_add(19, 6, json.dumps({"rotation": encoder_value}))
    return (encoder_value, encoder_pressed)

def convert_to_iso(data):
    for record in data:
        if isinstance(record['timestamp'], datetime):
            record['timestamp'] = record['timestamp'].isoformat()
    return data

def power_callback(pin):
    press_time = time.time()*1000
    print("counting for poweroff")
    while b1.is_pressed:
        if time.time()*1000 >= press_time + 3000:
            power_off()

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
                total_hits = DataRepository.hit_count()
                print(total_hits["count"])
                scoreboard.display_number(total_hits["count"])
        time.sleep(0.01)  # Small delay to prevent CPU overuse

def course():
    global running_session, active_user, current_course, last_event_time
    buzzer.beep(frequency=500, duration=1)
    history_add(17, 3, json.dumps({"frequency": 500}))
    OLED.write_text("GO!")
    history_add(22, 8, json.dumps({"text": "GO!"}))
    sequence = json.loads(DataRepository.get_sequence(current_course)["sequence"])["sequence"]
    running_session = DataRepository.start_session(active_user, current_course)
    for i in sequence:
        if i[-1] in [str(i) for i in range(8)]:
            initial_state = last_event_time.copy()
            byte = 1 << int(i[-1])
            byte = ~byte & 0xFF
            TargetPCF.write_byte(byte)
            history_add(8+int(i[-1]), 2, json.dumps({"byte": bin(byte)}))
            print(bin(byte))
            while last_event_time[int(i[-1])] == initial_state[int(i[-1])]:
                time.sleep(0.1)
        else:
            initial_state = last_event_time.copy()
            TargetPCF.write_byte(0b00000000)
            buzzer.beep(frequency=1000, duration=1)
            history_add(17, 4, json.dumps({"frequency": 1000}))
            print("reload")
            while last_event_time == initial_state:
                time.sleep(0.1)
    TargetPCF.write_byte(0b11111111)
    DataRepository.stop_session(running_session)
    running_session = None
    print("done")

def control():
    global running_session, active_user, current_course
    b1.set_press_callback(power_callback)
    text = "Interface: address"
    for interface, ip in get_ips():
        text += f"\n{interface}: {ip}"
    while True:
        OLED.clear_display()
        OLED.write_text(text)
        history_add(22, 8, json.dumps({"text": text}))
        while not b2.is_pressed:
            time.sleep(0.1)
        users = [[item['id'], item['username']] for item in DataRepository.get_users()]
        active_user = OLED.menu_navigation(users, get_encoder_state)
        history_add(22, 8, json.dumps({"text": users}))
        print(f"Selected user: {active_user}")
        send_user()
        history_add(19, 7, json.dumps({"user": active_user}))
        courses = [[item['id'], item['name']] for item in DataRepository.get_courses()]
        current_course = OLED.menu_navigation(courses, get_encoder_state)
        history_add(22, 8, json.dumps({"text": courses}))
        print(f"Selected course: {current_course}")
        history_add(19, 7, json.dumps({"course": current_course}))

        start_course_thread()

        time.sleep(0.01)  # Small delay to prevent CPU overuse

def start_target_thread():
    target_thread = threading.Thread(target=target, daemon=True)
    target_thread.start()
    print("target_thread started")

def start_control_thread():
    control_thread = threading.Thread(target=control, daemon=True)
    control_thread.start()
    print("control_thread started")

def start_course_thread():
    course_thread = threading.Thread(target=course, daemon=True)
    course_thread.start()
    print("course_thread started")

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    send_user()
    history = DataRepository.read_history()
    history = convert_to_iso(history)
    emit('B2F_history', {'history': history}, broadcast=False)

@socketio.on('B2F_addCourse')
def add_course(course_data):
    courseid = DataRepository.add_course(course_data['coursename'],  json.dumps({"sequence": course_data['coursedata'].split(', ')}))
    print(courseid)
    emit('B2F_success', broadcast=False)

@socketio.on('B2F_addUser')
def add_user(userdata):
    userid = DataRepository.add_user(userdata['username'])
    print(userid)
    emit('B2F_success', broadcast=False)

@socketio.on('B2F_getCourses')
def web_get_courses():
    print('Getting courses')
    courses = DataRepository.get_courses()
    emit('B2F_courses', {'courses': courses}, broadcast=False)

@socketio.on('B2F_getUsers')
def web_get_users():
    print('Getting users')
    users = DataRepository.get_users()
    emit('B2F_users', {'users': users}, broadcast=False)

@socketio.on('B2F_startCourse')
def web_start_course(id):
    global current_course
    current_course = id['courseid']
    emit('B2F_success', broadcast=False)
    start_course_thread()
    
@socketio.on('B2F_changeUser')
def web_change_user(id):
    global active_user
    active_user = id['userid']
    emit('B2F_success', broadcast=False)

@socketio.on('B2F_getUser')
def web_get_user():
    send_user()

@socketio.on('B2F_powerOff')
def web_power_off():
    emit('B2F_success', broadcast=False)
    power_off()

def cleanup():
    MCP.close()
    OLED.close()
    scoreboard.cleanup()

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
