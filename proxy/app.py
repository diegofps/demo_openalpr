#!/usr/bin/python3

from flask import jsonify, Flask, request, Response, jsonify
from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Process, Pool
from collections import defaultdict

import jsonpickle
import traceback
import requests
import random
import atexit
import json
import time
import sys
import os


### VARIABLES
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_TARGET", "openalpr")
CLIENT_CRT = os.getenv("CLIENT_CRT", "./tls/client-admin.crt")
CLIENT_KEY = os.getenv("CLIENT_KEY", "./tls/client-admin.key")
SERVER_CRT = os.getenv("SERVER_CRT", "./tls/server-ca.crt")
SSH_USER = os.getenv("SSH_USER", "ngd")
NUM_THREADS = int(os.getenv("NUM_THREADS", "16"))
REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "1"))

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
TARGET = 'http://localhost:4568/'
SERVER = "http://localhost:4569"

hit_counter = defaultdict(int)
app = Flask(__name__)
global_nodes = []


class Node:

    def __init__(self, ip):
        self.name = "Unknown"
        self.score_sum = 0.0
        self.score = 0.0
        self.pods = set()
        self.idle = 0.0
        self.busy = 1.0
        self.pod = 0
        self.ip = ip
    
    def add(self, podIP):
        self.pods.add(podIP)
    
    def __getstate__(self):
        return self.__dict__

def pick_node_and_pod():

    nodes_list = global_nodes
    print("Choosing between", len(nodes_list), "nodes")
    
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
    
    print("Chose node", cur, "and pod", node.pod)
    pod = node.pods[node.pod]
    node.pod += 1
    
    if node.pod == len(node.pods):
        node.pod = 0
    
    return node, pod

    
def get_node_stats(node):

    name = "Unknown"
    idle = 0.0
    busy = 1.0
    
    addr = node.ip if SSH_USER == '' else SSH_USER + '@' + node.ip
    cmd = ['ssh', addr, 'mpstat 1 1 -o JSON']
    cp = Popen(cmd, stdout=PIPE)
    
    try:
        cp.wait(timeout=5)
    except TimeoutExpired:
        print("Timeout")
        return name, idle, busy
    
    stdout = cp.stdout.read()
    
    if not b'not found' in stdout:
        try:
            data = json.loads(stdout)
            idle = data["sysstat"]["hosts"][0]["statistics"][0]['cpu-load'][0]['idle'] / 100.
            name = data["sysstat"]["hosts"][0]["nodename"]
            busy = 1.0 - idle
        except:
            traceback.print_exc(file=sys.stdout)
    
    return name, idle, busy

def detect_nodes_and_pods():

    r = requests.get("https://localhost:6443/api/v1/pods?labelSelector='app=" + DEPLOYMENT_NAME + "'", 
            cert=(CLIENT_CRT, CLIENT_KEY), 
            verify=SERVER_CRT)
    
    data = r.json()
    nodes = {}
    
    isReady = lambda item: not any(x["ready"] == False for x in item["status"]["containerStatuses"])
    
    for item in data["items"]:
        hostIP = item["status"]["hostIP"]
        podIP = item["status"]["podIP"]
        
        if not isReady(item):
            continue
        
        if not hostIP in nodes:
            nodes[hostIP] = Node(hostIP)
        
        node = nodes[hostIP]
        node.add(podIP)
    
    return list(nodes.values())

def refresh_nodes_stats(nodes_list):

    nodes_stats = p.map(get_node_stats, nodes_list)
    
    for node, stats in zip(nodes_list, nodes_stats):
        node.name = stats[0]
        node.idle = stats[1]
        node.busy = stats[2]
    
    score_sum = 0.0
    
    for node in nodes_list:
        score_sum += node.idle
        node.score_sum = score_sum
    
    for node in nodes_list:
        node.score_sum /= score_sum
        node.score = node.idle / score_sum
        #print(node.score_sum, node.score, node.idle)
    

### UPDATE 'CRON'
def sync_clock():

    while True:
        try:
            time.sleep(REFRESH_SECONDS)
            print("Pulse")
            r = requests.get(SERVER + "/sync")
            print(r.json())
        except KeyboardInterrupt:
            break
        except:
            print("Sync has failed")
            traceback.print_exc(file=sys.stdout)


### PARALLEL WORKERS (MUST APPEAR HERE OTHERWISE EVERYTHING ABOVE WILL NOT BE RECOGNIZED)
def close_running_threads():

    p.terminate()
    p.join()
    p.close()

atexit.register(close_running_threads)
sync_clock_process = Process(target=sync_clock)
sync_clock_process.start()
p = Pool(NUM_THREADS)

### WEB SERVER
@app.route('/sync', methods=["GET"])
def sync():

    start_time = time.monotonic()
    
    nodes_list = detect_nodes_and_pods()
    refresh_nodes_stats(nodes_list)
    
    global global_nodes
    global_nodes = nodes_list
    
    ellapsed_time = time.monotonic() - start_time
    
    body = jsonpickle.encode(
        {'nodes': nodes_list, 'ellapsed': ellapsed_time}, 
        unpicklable=False
    )
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )
    
    #return jsonify({
    #    "nodes": nodes.__dict__,
    #    "ellapsed": ellapsed_time
    #})

@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def proxy(path):

    #print("path=", path)
    #print("args=", str(request.args))
    #print("url=", request.url)
    #print("host_url=", request.host_url)
    #print("url2=", request.url.replace(request.host_url, 'https://wespa.com.br/'))
    node, pod = pick_node_and_pod()
    
    target = 'http://' + pod + ':4568/'
    print("Directing to ", target)
    hit_counter[node.ip] += 1
    
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, target),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in EXCLUDED_HEADERS]

    #body = resp.content
    body = resp.iter_content(chunk_size=10*1024)
    
    response = Response(body, resp.status_code, headers)
    
    return response

