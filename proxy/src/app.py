#!/usr/bin/python3

from flask import Flask

import strategies
import jsonpickle
import requests
import random
import params
import time


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

strategy = strategies.start()
app = Flask(__name__)


@app.route('/nodes', methods=["GET"])
def nodes():
    body = jsonpickle.encode(strategy.nodes, unpicklable=False)
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )


@app.route('/forward', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/forward/<path:path>', methods=HTTP_METHODS)
def proxy(path):
    return strategy.forward(path)
