from flask import request, Response
from threading import Thread
from models import Node, Pod
from utils import debug

import clustertools
import apiserver
import traceback
import requests
import random
import params
import time
import sys


EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']


class BaseSync(Thread):

    def __init__(self):
        super().__init__()
        self.listener = None
    
    def set_listener(self, listener):
        self.listener = listener
    
    def run(self):
        sleep_before = int(random.random() * params.REFRESH_SECONDS)
        sleep_after  = params.REFRESH_SECONDS - sleep_before
        
        while True:
            try:
                time.sleep(sleep_before)
                print("Starting sync")
                self.sync()
                print("Sync ended")
                time.sleep(sleep_after)
                
            except KeyboardInterrupt:
                print("Bye")
                sys.exit(0)
                break
            
            except:
                debug("Sync has failed")
                traceback.print_exc(file=sys.stdout)
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        self.listener.refresh_nodes(nodes)

    def detect_nodes_and_pods(self):
        nodes_data = apiserver.get_nodes()
        pods_data  = apiserver.get_pods()

        nodes = [Node(x) for x in nodes_data]
        pods  = [Pod(x) for x in pods_data]

        nodes_map = {x.ip:x for x in nodes}
        
        for p in pods:

            if not p.isReady:
                print("Pod is not ready, skipping")
                continue
            
            if not p.hostIP in nodes_map:
                print("Pod is attached to an unknown host, skipping:", p.hostIP)
                continue
            
            nodes_map[p.hostIP].add(p)
        
        return [x for x in nodes if x.pods]


    def refresh_cpu_stats(self, nodes, onlyPrimary=False):
        if onlyPrimary:
            nodes = [x for x in nodes if x.primary]
        
        for node in nodes:
            _, idle, busy, _, _ = clustertools.get_stats(node.ip)
            node.idle = idle
            node.busy = busy


class BaseStrategy:
    
    def __init__(self, sync=BaseSync()):
        self.sync  = sync
        self.nodes = []
        sync.set_listener(self)
        sync.start()
    
    def refresh_scores(self, nodes_list):
        score_sum = 0.0
        
        for node in nodes_list:
            score_sum += node.score_raw
            node.score_sum = score_sum
        
        if score_sum == 0.0:
            print("Zeroed score_sum, changing to 1.0")
            score_sum = 1.0
        
        for node in nodes_list:
            node.score_sum /= score_sum
            node.score = node.score_raw / score_sum

    def refresh_nodes(self, new_nodes, busy=False):
        self.nodes = new_nodes

    def pick_node_and_pod(self):
        raise NotImplementedError("When subclassing BaseStrategy you must implement pick_node_and_pod to reflect your own strategy")
    
    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        response  = self.forward_to(node, pod)
        return response
    
    def forward_to(self, node, pod):
        target = 'http://' + pod.ip + ':4568/'
        newurl = request.url.replace(request.host_url + "forward/", target)
        
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

        return Response(body, resp.status_code, headers)
