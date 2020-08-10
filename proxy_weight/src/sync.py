from multiprocessing import Process, Pool
from models import Node, Pod
from utils import debug

import clustertools
import jsonpickle
import apiserver
import traceback
import requests
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


def refresh_cpu_stats(nodes):
    for node in nodes:
        _, idle, busy, _, _ = clustertools.get_stats(node.ip)
        node.idle = idle
        node.busy = busy


def refresh_scores(nodes_list):
    score_sum = 0.0
    
    for node in nodes_list:
        score_sum += node.score_raw
        node.score_sum = score_sum
    
    # debug("Score sum was", score_sum)
    
    if score_sum == 0.0:
        debug("Zeroed score_sum, changing to 1.0")
        score_sum = 1.0
    
    for node in nodes_list:
        node.score_sum /= score_sum
        node.score = node.score_raw / score_sum
        # debug(node.score_sum, node.score, node.idle)


def sync(p):
    nodes = detect_nodes_and_pods()
    # print("FOUND", len(nodes), "NODES")

    # Refresh score_raw using cpu data
    # refresh_cpu_stats(nodes)
    # for node in nodes:
    #     node.score_raw = 1.0 if node.idle >= 0.9 else node.idle / 0.9
    #     node.score_raw *= node.cpus
    
    # Refresh score_raw using weight
    for node in nodes:
        node.score_raw = node.weight
    
    refresh_scores(nodes)

    data = jsonpickle.encode(nodes)
    # print("SENDING DATA TO SERVER/PROXY_DATA", data)

    headers = {'content-type': 'application/json'}
    url = params.SELF_SERVER + "/proxy_data"
    r = requests.post(url, data=data, headers=headers)
    
    # debug(r.json())


def sync_loop():
    p = Pool(params.NUM_THREADS)
    
    while True:
        try:
            time.sleep(params.REFRESH_SECONDS)
            debug("Running sync")
            sync(p)
        except KeyboardInterrupt:
            p.terminate()
            p.join()
            p.close()
            break
        except:
            debug("Sync has failed")
            traceback.print_exc(file=sys.stdout)


sync_clock_process = Process(target=sync_loop)


def start():
    if not sync_clock_process.is_alive():
        sync_clock_process.start()
