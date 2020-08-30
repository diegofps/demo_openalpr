from strategies.base_strategy import BaseStrategy, BaseSync
from collections import defaultdict
from utils import debug, MovingAverage

import random
import time


class SyncMin(BaseSync):

    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        self.listener.refresh_nodes(nodes)


class MinStrategy(BaseStrategy):

    def __init__(self):
        super().__init__(SyncMin())
        self.avgs = defaultdict(MovingAverage)
    
    def refresh_nodes(self, new_nodes, busy=False):
        self.nodes = new_nodes

    def pick_node_and_pod(self):
        nodes  = self.nodes
        weight = 0
        idx    = None
        tmp    = []

        for node in nodes:
            cur = self.avgs[node.ip].read()
            tmp.append(node.ip + ":" + str(cur))

            if idx is None or cur < weight:
                weight = cur
                idx = node

        opts = [x for x in nodes if self.avgs[x.ip].read() - weight < 100]

        node = random.choice(opts)
        pod = random.choice(node.pods)
        debug("MINS:", " ".join(tmp))
        debug("CHOSE:", node.ip)
        return node, pod

    def pick_node_and_pod_1(self):
        nodes  = self.nodes
        weight = 0
        idx    = None
        tmp    = []
        
        for node in nodes:
            cur = self.avgs[node.ip].read()
            tmp.append(node.ip + ":" + str(cur))

            if idx is None or cur < weight:
                weight = cur
                idx = node
       
        node = idx
        pod = random.choice(node.pods)
        debug("MINS:", " ".join(tmp))
        debug("CHOSE:", node.ip)
        return node, pod


    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        avg = self.avgs[node.ip]

        start_time = time.monotonic()
        response = self.forward_to(node, pod)
        ellapsed_time = time.monotonic() - start_time

        avg.write(ellapsed_time)
        
        return response
