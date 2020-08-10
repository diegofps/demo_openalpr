#!/usr/bin/python3

from flask import jsonify, Flask, request, Response, jsonify
from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Process, Pool
from collections import defaultdict

import jsonpickle
import traceback
import requests
import random
import shlex
import json
import time
import sys
import os


DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "openalpr")
CLIENT_CRT      = os.getenv("CLIENT_CRT", "./tls/client-admin.crt")
CLIENT_KEY      = os.getenv("CLIENT_KEY", "./tls/client-admin.key")
SERVER_CRT      = os.getenv("SERVER_CRT", "./tls/server-ca.crt")
SSH_USER        = os.getenv("SSH_USER", "ngd")
SSH_PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY", "~/.ssh/id_rsa")
API_SERVER      = os.getenv("API_SERVER", "https://192.168.1.134:6443")
SELF_SERVER     = os.getenv("SELF_SERVER", "http://localhost:4570")
NUM_THREADS     = int(os.getenv("NUM_THREADS", "16"))
REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "1"))

app = Flask(__name__)
nodes = []


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


def debug(*args, author=None):
    if author:
        print(author, "|", *args, file=sys.stderr)
    else:
        print(*args, file=sys.stderr)
    sys.stdout.flush()


def get_node_stats(node):
    debug("Get nodes stats")
    
    name = "Unknown"
    arch = "Unknown"
    idle = 0.0
    busy = 1.0
    cpus = 1
    
    addr = node.ip if SSH_USER == '' else SSH_USER + '@' + node.ip
    
    cmd = "ssh -o \"StrictHostKeyChecking no\" -i {} {} 'mpstat 1 1 -o JSON'".format(SSH_PRIVATE_KEY, addr)
    debug(cmd)
    cmd = shlex.split(cmd)
    
    with Popen(cmd, stdout=PIPE) as proc:
        try:
            stdout, err = proc.communicate(timeout=3)
        except TimeoutExpired:
            proc.kill()
            stdout, err = proc.communicate()
    
    if b'not found' in stdout:
        debug("not found")
        return name, idle, busy, arch, cpus
    
    try:
        data = json.loads(stdout)
        host = data["sysstat"]["hosts"][0]
        
        idle = host["statistics"][0]['cpu-load'][0]['idle'] / 100.
        name = host["nodename"]
        arch = host["machine"]
        cpus = host["number-of-cpus"]
        busy = 1.0 - idle
        debug("success")
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


def refresh_nodes_stats(nodes_list, p):
    debug("REFRESHING NODES")
    #nodes_stats = p.map(get_node_stats, nodes_list)
    nodes_stats = [get_node_stats(x) for x in nodes_list]
    debug("NODES REFRESHED", nodes_stats)
    
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
    
    debug("Score sum was", score_sum)
    
    if score_sum == 0.0:
        score_sum = 1.0
    else:
        debug("score_sum seems fine:", score_sum)
    
    for node in nodes_list:
        node.score_sum /= score_sum
        node.score = node.score_raw / score_sum
        debug(node.score_sum, node.score, node.idle)


def sync(p):

    nodes_list = detect_nodes_and_pods()
    debug("Nodes detected", len(nodes_list))
    refresh_nodes_stats(nodes_list, p)
    debug("Nodes refreshed")
    
    data = jsonpickle.encode(nodes_list)
    headers = {'content-type': 'application/json'}
    url = SELF_SERVER + "/route"
    r = requests.post(url, data=data, headers=headers)
    
    debug(r.json())

def pulse_sync():
    p = Pool(NUM_THREADS)
    
    while True:
        try:
            time.sleep(REFRESH_SECONDS)
            debug("Pulse")
            sync(p)
        except KeyboardInterrupt:
            p.terminate()
            p.join()
            p.close()
            break
        except:
            debug("Sync has failed")
            traceback.print_exc(file=sys.stdout)


### PARALLEL WORKERS (MUST APPEAR HERE OTHERWISE EVERYTHING ABOVE WILL NOT BE RECOGNIZED)
sync_clock_process = Process(target=pulse_sync)
sync_clock_process.start()


### WEB SERVER

@app.route('/route', methods=["POST"])
def post_route():
    data = jsonpickle.decode(request.data)
    debug("RECEIVED", data)
    
    global nodes
    nodes = data
    
    body = jsonpickle.encode(data, unpicklable=False)
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )


@app.route('/route', methods=["GET"])
def get_route():
    body = jsonpickle.encode(nodes, unpicklable=False)
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )

