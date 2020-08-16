from strategies.base_strategy import BaseStrategy, BaseSync
from collections import defaultdict
from utils import MovingAverage

import random
import time


class MinStrategy(BaseStrategy):

    def __init__(self):
        super().__init__(SyncMin())
        self.avgs = defaultdict(MovingAverage)
    
    def refresh_nodes(self, new_nodes, busy=False):
        self.nodes = new_nodes

    def pick_node_and_pod(self):
        nodes  = self.nodes
        weight = 0
        idx    = -1
        
        for i, node in enumerate(nodes):
            cur = self.avgs[node.ip].read()
            if idx == -1 or cur < weight:
                weight = cur
                idx = i
        
        pod = random.choice(node.pods)
        return node, pod


    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        avg = self.avgs[node.ip]

        start_time = time.monotonic()
        response = self.forward_to(node, pod)
        ellapsed_time = time.monotonic() - start_time

        avg.write(ellapsed_time)
        
        return response


class SyncMin(BaseSync):

    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        self.listener.refresh_nodes(nodes)
