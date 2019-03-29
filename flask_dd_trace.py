from flask import Flask
from flask import request as flask_request
#import logging
import sys
import blinker as _
import time

import mysql.connector
import json

from logging.config import dictConfig

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import Pin, patch, patch_all

# DogStatsD
from datadog import statsd

patch_all(logging=True, mysql=True, flask=False)

with tracer.trace("web.request", service="kikeyama_service") as span:
  span.set_tag("source", "flask_apm")

## Have flask use stdout as the logger
#patch(logging=True)
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': FORMAT,
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': '/var/log/flask_dd_trace.log',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

## Trace patch for MySQL
#patch(mysql=True)

## Connecting MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="python",
    passwd="password",
    database="kikeyama"
)
mycursor = mydb.cursor()

## Use a pin to specify metadata related to this connection
Pin.override(mydb, service='kikeyama_mysql')

## Flask
app = Flask(__name__)
#traced_app = TraceMiddleware(app, tracer, service="kikeyama_service", distributed_tracing=False)
traced_app = TraceMiddleware(app, tracer, service='kikeyama_service')

@app.route('/')
def api_entry():
    start_time = time.time()

    app.logger.info('getting root endpoint')
#    return 'Entrypoint to the Application'
    name = flask_request.args.get('name', str)
    mycursor.execute("SELECT Name, UUID, Number FROM kikeyama_python where name='%s'" % name)
    myresult = mycursor.fetchall()
    
    for x in myresult:
        result = json.dumps(x)
        return result

    duration = time.time() - start_time
    statsd.distribution('kikeyama.dogstatsd.distribution.latency', duration)
    statsd.histogram('kikeyama.dogstatsd.histogram.latency', duration)

@app.route('/api/apm')
def apm_endpoint():
    app.logger.info('getting apm endpoint')
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    app.logger.info('getting trace endpoint')
    return 'Posting Traces'

if __name__ == '__main__':
    app.logger.info('%(message)s This is __main__ log')
    app.run(host='0.0.0.0', port='5050')
