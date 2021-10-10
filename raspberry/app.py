import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from flask import Flask

# Sensor setup
sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BOARD)
 
# GPIO where the sensor will be connected
sensorPin = 2

# Creates a webserver
app = Flask(__name__)

@app.route('/metrics')
def metrics():
    umid, temp = Adafruit_DHT.read_retry(sensor, sensorPin)
    if umid is not None and temp is not None:
        return '# HELP local_temp local temperature\n# TYPE local_temp gauge\nlocal_temp {}\n# HELP local_umid local umid\n# TYPE local_umid gauge\nlocal_umid {}\n'.format(int(temp), int(umid)), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return 'Couldn\'t read data from DHT11 !!!', 200, {'Content-Type': 'text/plain; charset=utf-8'}