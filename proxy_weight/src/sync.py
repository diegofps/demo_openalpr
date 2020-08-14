from multiprocessing import Process
from threading import Thread
from models import Node, Pod
from utils import debug

import clustertools
import jsonpickle
import apiserver
import traceback
import requests
import random
import params
import time
import sys


def detect_nodes_and_pods():
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


def refresh_cpu_stats(p, nodes, onlyPrimary=False):
    if onlyPrimary:
        nodes = [x for x in nodes if x.primary]
    
    for node in nodes:
        _, idle, busy, _, _ = clustertools.get_stats(node.ip)
        node.idle = idle
        node.busy = busy


class BaseSync(Thread):

    def __init__(self):
        super().__init__()
        #self.p = Pool(params.NUM_THREADS)
        self.listener = None
        self.p = None
    
    def set_listener(self, listener):
        self.listener = listener
    
    def run(self):
        sleep_before = int(random.random() * params.REFRESH_SECONDS)
        sleep_after  = params.REFRESH_SECONDS - sleep_before
        
        while True:
            try:
                time.sleep(sleep_before)
                debug("Starting sync")
                self.sync()
                debug("Sync ended")
                time.sleep(sleep_after)
                
            except KeyboardInterrupt:
                debug("Bye")
                sys.exit(0)
                #self.p.terminate()
                #self.p.join()
                #self.p.close()
                break
            
            except:
                debug("Sync has failed")
                traceback.print_exc(file=sys.stdout)


class SyncWeight(BaseSync):
    
    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = detect_nodes_and_pods()

        # Refresh score_raw using weight
        for node in nodes:
            node.score_raw = node.weight
        
        self.listener(nodes, busy=True)

        # Send nodes and weights for server
        #data = jsonpickle.encode(nodes)
        
        #headers = {'content-type': 'application/json'}
        #url = params.SELF_SERVER + "/proxy_data"
        #r = requests.post(url, data=data, headers=headers)

        debug("SyncWeight completed, found", len(nodes), "nodes")


class SyncWeightOnBusy(BaseSync):

    def __init__(self):
        super().__init__()

    def sync(self):
        nodes = detect_nodes_and_pods()
        refresh_cpu_stats(None, nodes, onlyPrimary=True)
        
        # Calculate average cpu usage in primary nodes
        sumCpu = 0.0
        numCpu = 0
        
        for n in nodes:
            if n.primary:
                sumCpu += n.busy
                numCpu += 1
        
        if numCpu == 0:
            debug("Warning: No primary node detected")
            avgCpu = 1.0
            
        else:
            avgCpu = sumCpu / numCpu
        
        # Update the scores
        if avgCpu >= params.MIN_CPU_FOR_WEIGHT:
            print("CPU usage is high, enabling CSDs (CPU:", avgCpu, ", Nodes:", len(nodes), ")")

            for node in nodes:
                node.score_raw = node.weight

            self.listener(nodes, busy=True)
        
        else:
            print("CPU usage is low, using only primary nodes (CPU:", avgCpu, ", Nodes:", len(nodes), ")")
            
            for node in nodes:
                if node.primary:
                    node.score_raw = node.weight
                else:
                    node.score_raw = 0.0
            
            self.listener(nodes, busy=False)
        

        # Send the nodes and their weights to our remote server
        #data = jsonpickle.encode(nodes)

        #headers = {'content-type': 'application/json'}
        #url = params.SELF_SERVER + "/proxy_data"
        #r = requests.post(url, data=data, headers=headers)

        debug("SyncWeight completed, found", len(nodes), "nodes")


class SyncAdaptiveWeightOnBusy(BaseSync):

    def __init__(self):
        super().__init__()

    def sync(self):
        pass


if params.SYNC == "WEIGHT":
    sync_process = SyncWeight()

elif params.SYNC == "WEIGHT_ON_BUSY":
    sync_process = SyncWeightOnBusy()

elif params.SYNC == "ADAPTIVE_WEIGHT_ON_BUSY":
    sync_process = SyncWeightOnBusy()

else:
    debug("Unknown sync method (", params.SYNC, "), using default method: WEIGHT")
    sync_process = SyncWeight()


def start(listener):
    sync_process.set_listener(listener)
    if not sync_process.is_alive():
        sync_process.start()


