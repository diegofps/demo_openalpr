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
import shlex
import json
import time
import sys
import os


### VARIABLES
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "openalpr")
CLIENT_CRT = os.getenv("CLIENT_CRT", "./tls/client-admin.crt")
CLIENT_KEY = os.getenv("CLIENT_KEY", "./tls/client-admin.key")
SERVER_CRT = os.getenv("SERVER_CRT", "./tls/server-ca.crt")
SSH_USER = os.getenv("SSH_USER", "ngd")
SSH_PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY", "~/.ssh/id_rsa")
NUM_THREADS = int(os.getenv("NUM_THREADS", "16"))
REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "1"))
API_SERVER = os.getenv("API_SERVER", "https://192.168.1.134:6443")
SELF_SERVER = os.getenv("SELF_SERVER", "http://localhost:4569")

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']

hit_counter = defaultdict(int)
app = Flask(__name__)
global_nodes = []

def debug(*args, author=None):
    if author:
        print(author, "|", *args, file=sys.stderr)
    else:
        print(*args, file=sys.stderr)
    sys.stdout.flush()


class Node:

    def __init__(self, ip):
        self.name = "Unknown"
        self.arch = "Unknown"
        self.score_sum = 0.0
        self.score_raw = 0.0
        self.score = 0.0
        self.pods = []
        self.idle = 0.0
        self.busy = 1.0
        self.pod = 0
        self.ip = ip
    
    def add(self, podIP):
        self.pods.append(podIP)
    
    def __getstate__(self):
        return self.__dict__

def pick_node_and_pod():

    nodes_list = global_nodes
    debug("Choosing between", len(nodes_list), "nodes")
    
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
    
    #debug("Chose node", cur, "and pod", node.pod)
    pod = node.pods[node.pod]
    node.pod += 1
    
    if node.pod == len(node.pods):
        node.pod = 0
    
    return node, pod


def get_node_stats(node):
    #debug("Starting get_node_stats")

    name = "Unknown"
    arch = "Unknown"
    idle = 0.0
    busy = 1.0
    cpus = 1
    
    addr = node.ip if SSH_USER == '' else SSH_USER + '@' + node.ip
    cmd = "ssh -o \"StrictHostKeyChecking no\" -i {} {} 'mpstat 1 1 -o JSON'".format(SSH_PRIVATE_KEY, addr)
    #debug("SSH CMD:", cmd)
    cmd = shlex.split(cmd)
    
    with Popen(cmd, stdout=PIPE) as proc:
        try:
            stdout, err = proc.communicate(timeout=3)
        except TimeoutExpired:
            proc.kill()
            stdout, err = proc.communicate()
    
    
    #debug("SSH RESPONSE:", stdout)
    
    if b'not found' in stdout:
        #debug("COMMAND NOT FOUND:", stdout, author=node.ip)
        return name, idle, busy, arch, cpus
    
    try:
        data = json.loads(stdout)
        host = data["sysstat"]["hosts"][0]
        
        idle = host["statistics"][0]['cpu-load'][0]['idle'] / 100.
        name = host["nodename"]
        arch = host["machine"]
        cpus = host["number-of-cpus"]
        busy = 1.0 - idle
        #debug(node.ip + "| SSH RESPONSE IS GOOD")
    except:
        debug("CORRUPTED JSON IN RESPONSE: " + stdout, author=node.ip)
        traceback.print_exc(file=sys.stdout)
    
    return name, idle, busy, arch, cpus

def isReady(item):
    if not "status" in item:
        return False
    
    if not "containerStatuses" in item["status"]:
        return False
    
    if not "podIP" in item["status"]:
        return False
    
    if not "hostIP" in item["status"]:
        return False
    
    if any(x["ready"] == False for x in item["status"]["containerStatuses"]):
        return False
    
    return True

def detect_nodes_and_pods():

    r = requests.get(API_SERVER + "/api/v1/pods?labelSelector=app=" + DEPLOYMENT_NAME, 
            cert=(CLIENT_CRT, CLIENT_KEY), 
            verify=SERVER_CRT)
    
    data = r.json()
    #debug("APISERVER RESPONSE:", data)
    nodes = {}
    
    for item in data["items"]:
    
        if not isReady(item):
            continue
        
        hostIP = item["status"]["hostIP"]
        podIP = item["status"]["podIP"]
        
        if not hostIP in nodes:
            nodes[hostIP] = Node(hostIP)
        
        node = nodes[hostIP]
        node.add(podIP)
    
    return list(nodes.values())

def refresh_nodes_stats(nodes_list):
    #debug("REFRESHING NODES")
    nodes_stats = p.map(get_node_stats, nodes_list)
    #nodes_stats = [get_node_stats(x) for x in nodes_list]
    #debug("NODES REFRESHED", nodes_stats)
    
    for node, stats in zip(nodes_list, nodes_stats):
        node.name = stats[0]
        node.idle = stats[1]
        node.busy = stats[2]
        node.arch = stats[3]
        node.cpus = stats[4]
    
    score_sum = 0.0
    
    for node in nodes_list:
        node.score_raw = 1.0 if node.idle >= 0.9 else node.idle / 0.9
        node.score_raw *= node.cpus
        score_sum += node.score_raw
        node.score_sum = score_sum
    
    #debug("Score sum was", score_sum)
    
    if score_sum == 0.0:
        score_sum = 1.0
    else:
        debug("score_sum seems fine:", score_sum)
    
    for node in nodes_list:
        node.score_sum /= score_sum
        node.score = node.score_raw / score_sum
        #debug(node.score_sum, node.score, node.idle)


### 'cron' like process
def sync_clock():

    while True:
        try:
            time.sleep(REFRESH_SECONDS)
            debug("Pulse")
            r = requests.get(SELF_SERVER + "/sync")
            debug(r.json())
        except KeyboardInterrupt:
            break
        except:
            debug("Sync has failed")
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

@app.route('/status', methods=["GET"])
def status():
    debug("Starting /status")
    global global_nodes
    response = []
    
    for node in global_nodes:
        response.append({
            "name": node.name,
            "ip": node.ip,
            "num_pods": len(node.pods),
            "pod_id": node.pod,
            "score": node.score,
            "busy": node.busy
        })
    
    return jsonify(response)


### WEB SERVER
@app.route('/sync', methods=["GET"])
def sync():
    #debug("Starting /Sync")
    start_time = time.monotonic()
    
    nodes_list = detect_nodes_and_pods()
    debug("SYNC: Found", len(nodes_list), "nodes")
    
    refresh_nodes_stats(nodes_list)
    #debug("Stats refreshed")
    
    global global_nodes
    global_nodes = nodes_list
    #debug("Global nodes list refreshed")
    
    ellapsed_time = time.monotonic() - start_time
    
    body = jsonpickle.encode(
        {'nodes': nodes_list, 'ellapsed': ellapsed_time}, 
        unpicklable=False
    )
    
    #debug("Body prepared")
    
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
    debug("Directing to ", target)
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

