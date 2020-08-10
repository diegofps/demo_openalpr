#!/usr/bin/python3

from flask import jsonify, Flask, request, Response, jsonify
from utils import debug

import jsonpickle
import requests
import random
import sync


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']


app = Flask(__name__)
sync.start()
nodes = []


def pick_node_and_pod():
    nodes_list = nodes
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
    
    pod = random.choice(node.pods)
    node.pod += 1
    
    if node.pod == len(node.pods):
        node.pod = 0
    
    print("Chose node", node.name, node.ip, "and pod", pod.name, pod.ip)
    return node, pod


@app.route('/proxy_data', methods=["POST"])
def post_route():
    data = jsonpickle.decode(request.data)
    # debug("RECEIVED FROM CLIENT", data)
    
    global nodes
    nodes = data
    
    body = jsonpickle.encode(data, unpicklable=False)
    
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )


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

    #print("path=", path)
    #print("args=", str(request.args))
    #print("url=", request.url)
    #print("host_url=", request.host_url)
    #print("url2=", request.url.replace(request.host_url, 'https://wespa.com.br/'))
    node, pod = pick_node_and_pod()
    
    target = 'http://' + pod.ip + ':4568/'
    #debug("Directing to ", target)
    #hit_counter[node.ip] += 1

    newurl = request.url.replace(request.host_url + "forward/", target)
    print(newurl)
    
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
    
    return response
