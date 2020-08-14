#!/usr/bin/python3

from flask import jsonify, Flask, request, Response, jsonify
from collections import defaultdict
from utils import debug

import jsonpickle
import requests
import random
import params
import sync
import time


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']


class MovingAverage:

    def __init__(self):
        self.values = [1 for _ in range(params.MOVING_AVERAGE_LEN)]
        self.p = 0
    
    def write(self, value):
        self.values[self.p] = value
        self.p += 1

        if self.p == params.MOVING_AVERAGE_LEN:
            self.p = 0
    
    def read(self):
        return sum(self.values) / params.MOVING_AVERAGE_LEN


avgs  = defaultdict(MovingAverage)
app   = Flask(__name__)
nodes = []


def refresh_scores(nodes_list):
    score_sum = 0.0
    
    for node in nodes_list:
        score_sum += node.score_raw
        node.score_sum = score_sum
    
    if score_sum == 0.0:
        debug("Zeroed score_sum, changing to 1.0")
        score_sum = 1.0
    
    for node in nodes_list:
        node.score_sum /= score_sum
        node.score = node.score_raw / score_sum


def node_listener(new_nodes, busy=False):
    if busy and params.SYNC == "ADAPTIVE_WEIGHT_ON_BUSY":
        tmp = []
        for n in new_nodes:
            n.score_raw = avgs[n.ip].read()
            tmp.append(n.ip + ":" + str(n.score_raw))
        print("Applying Adaptive Weight: ", " ".join(tmp))
    
    global nodes

    refresh_scores(new_nodes)
    nodes = new_nodes

sync.start(node_listener)


def pick_node_and_pod():
    nodes_list = nodes
    #debug("Choosing between", len(nodes_list), "nodes")
    
    if not nodes_list:
        return None
    
    if len(nodes_list) == 1:
        node = nodes_list[0]
    
    else:
        r = random.random()
        cur = 0
        
        while r > nodes_list[cur].score_sum:
            cur += 1
        
        node = nodes_list[cur]
    
    pod = random.choice(node.pods)
    node.pod += 1
    
    if node.pod == len(node.pods):
        node.pod = 0
    
    print("Chose node", node.name, node.ip, "and pod", pod.name, pod.ip)
    return node, pod


@app.route('/proxy_data', methods=["GET"])
def get_route():
    body = jsonpickle.encode(nodes, unpicklable=False)
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )


@app.route('/forward', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/forward/<path:path>', methods=HTTP_METHODS)
def proxy(path):
    node, pod = pick_node_and_pod()
    target    = 'http://' + pod.ip + ':4568/'
    newurl    = request.url.replace(request.host_url + "forward/", target)
    
    start_time = time.monotonic()

    resp = requests.request(
        method=request.method,
        url=newurl,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in EXCLUDED_HEADERS]

    #body = resp.content
    body = resp.iter_content(chunk_size=10*1024)

    response = Response(body, resp.status_code, headers)
    
    ellapsed_time = time.monotonic() - start_time
    avgs[node.ip].write(ellapsed_time)
    
    return response
