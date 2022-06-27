# DHT11
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Defines the sensor and it's pin
sensor = Adafruit_DHT.DHT11
sensor_pin = 2 # this must match with the pin you connected the data wire.

# Add webserver
from flask import Flask, current_app
from flask_cors import CORS, cross_origin
import json
from datetime import date, datetime

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return current_app.send_static_file('index.html')

@app.route('/api', methods=['GET'], defaults={'dataFormat': None})
@app.route('/api/<string:dataFormat>', methods=['GET'])
@cross_origin()
def api(dataFormat):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    contentType = setContentType(dataFormat)

    humidity = validateBoundaries(humidity, 0, 100)
    temperature = validateBoundaries(temperature, 0, 125)

    if humidity != -255 or temperature != -255:
        return formatted_output(humidity, temperature, contentType), 200, {'Content-Type': contentType}
    else:
        return 'Could not read from DHT11.', 424, {'Content-Type': 'text/plain; charset=utf-8'}

# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def validateBoundaries(value, lower, upper):
    if value > lower and value < upper:
        return value
    return -255

def setContentType(dataFormat):
    if dataFormat is not None and dataFormat == "json":
        return 'application/json; charset=utf-8'
    return 'text/plain; charset=utf-8'

def formatted_output(humidity, temperature, contentType):
    if contentType is 'application/json; charset=utf-8':
        x = { "temperature" : temperature, "humidity": humidity, "datetime": datetime.now().isoformat() }
        return json.dumps(x, default=json_serial)
    return '# HELP local_temp local temperature\n# TYPE local_temp gauge\nlocal_temp {}\n# HELP local_humidity local humidity\n# TYPE local_humidity gauge\nlocal_humidity {}\n'.format(temperature, humidity)
