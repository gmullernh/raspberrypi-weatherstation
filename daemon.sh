#!/bin/bash
# flask settings
# https://stackoverflow.com/questions/6337119/how-do-you-daemonize-a-flask-application
export FLASK_APP=$PWD/app.py
export FLASK_DEBUG=0

# Expose to the network at port 5000
flask run --host=0.0.0.0 --port=5000