from strategies.weight_strategy import WeightStrategy
from collections import defaultdict
from utils import MovingAverage

import params
import time


def time_to_weight_1(n, v):
    return 1.0 / v

def time_to_weight_2(n, v):
    return 1.0 / (v * v)

def time_to_weight_3(n, v):
    return n.cpus / v

def time_to_weight_4(n, v):
    return n.cpus / v * 4 if n.arch == "amd64" else n.cpus / v


class AdaptiveWeightStrategy(WeightStrategy):

    def __init__(self):
        super().__init__()
        self.time_to_weight = globals()[params.TIME_TO_WEIGHT]
        self.avgs = defaultdict(MovingAverage)
    
    def refresh_nodes(self, new_nodes, busy=False):
        if not params.ON_BUSY or busy:
            for n in new_nodes:
                n.score_raw = self.time_to_weight(n, self.avgs[n.ip].read())
        
        self.refresh_scores(new_nodes)
        self.nodes = new_nodes

    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        avg = self.avgs[node.ip]

        start_time = time.monotonic()
        response = self.forward_to(node, pod)
        ellapsed_time = time.monotonic() - start_time

        avg.write(ellapsed_time)
        node.score_raw = self.time_to_weight(node, avg.read())
        self.refresh_scores(self.nodes)
        
        return response
