# DHT11
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Defines the sensor and it's pin
sensor = Adafruit_DHT.DHT11
sensor_pin = 2 # this must match with the pin you connected the data wire.

# Add webserver
from flask import Flask
from flask_cors import CORS, cross_origin
import json
from datetime import date, datetime

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'], defaults={'dataFormat': None})
@app.route('/api/<string:dataFormat>', methods=['GET'])
@cross_origin()
def metrics(dataFormat):
    umid, temp = Adafruit_DHT.read_retry(sensor, sensor_pin)
    x = { "temperature" : temp, "humidity": umid, "datetime": datetime.now().isoformat() }
    if umid is not None and temp is not None:
        if dataFormat is not None and dataFormat == "json":
            return json.dumps(x, default=json_serial), 200, {'Content-Type': 'application/json; charset=utf-8'}
        return '# HELP local_temp local temperature\n# TYPE local_temp gauge\nlocal_temp {}\n# HELP local_humidity local humidity\n# TYPE local_humidity gauge\nlocal_humidity {}\n'.format(int(temp), int(umid)), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return 'Could not read from DHT11.', 200, {'Content-Type': 'text/plain; charset=utf-8'}

# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
