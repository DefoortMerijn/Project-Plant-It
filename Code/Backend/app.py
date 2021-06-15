
import threading
from datetime import datetime, date
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, json, jsonify, request
from repositories.DataRepository import DataRepository


# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=False, engineio_logger=False, ping_timeout=1)

CORS(app)
# Custom endpoint
endpoint = '/api/v1'


@ app.route(endpoint + '/DeviceLog', methods=['GET', 'POST'])
def get_sensors():
    if request.method == 'GET':
        return jsonify(DataRepository.read_log()), 200
    elif request.method == 'POST':
        print('posten')
        data = DataRepository.json_or_formdata(request)
        new_log = DataRepository.create_log(data.get('Sensor'), data.get('Value'), data.get('Plant')
                                            )
        socketio.emit('B2F_new_data', {'data': data})
        return jsonify(readinglog=new_log), 201


@ app.route(endpoint + '/DeviceLog/Sensor/<sensor_id>', methods=['GET'])
def get_log(sensor_id):
    if request.method == 'GET':
        return jsonify(DataRepository.read_log_today(sensor_id)), 200


@ app.route(endpoint + '/DeviceLog/<sensor_id>', methods=['GET'])
def get_livefeed(sensor_id):
    if request.method == 'GET':
        return jsonify(DataRepository.read_livefeed_sensors(sensor_id)), 200


@app.route(endpoint + '/Plants', methods=['GET'])
def get_plants():
    if request.method == 'GET':
        return jsonify(DataRepository.read_name_plants()), 200


@app.route(endpoint + '/Water/<plant_id>', methods=['GET'])
def get_moisture_plants(plant_id):
    if request.method == 'GET':
        return jsonify(DataRepository.read_moisture_plant(plant_id)), 200


@app.route(endpoint + '/Timer', methods=['GET', 'POST'])
def get_timer():
    if request.method == 'GET':
        return jsonify(DataRepository.read_last_timer()), 200
    elif request.method == 'POST':
        print('posten alarm')
        data = DataRepository.json_or_formdata(request)
        nieuweTimer = DataRepository.add_timer(
            data.get('Name'), data.get('Time'), data.get('Day'), data.get('Plant'))
        return jsonify(Timer=nieuweTimer), 201


@app.route(endpoint + '/TimerMoisture', methods=['GET'])
def get_moisture_timer():
    if request.method == 'GET':
        return jsonify(DataRepository.get_moisture_for_alarm()), 200


@ socketio.on('connect')
def initial_connection():
    print('A new client connect')


@ socketio.on('F2B_send_water')
def send_water(moisture):
    print(moisture['Moisture'])
    emit('B2A_send_water', moisture, broadcast=True)


# ANDERE FUNCTIES
if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
