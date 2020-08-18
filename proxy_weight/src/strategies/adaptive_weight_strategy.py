from strategies.weight_strategy import WeightStrategy
from collections import defaultdict
from utils import MovingAverage

import time


def time_to_weight(n, v):
    #return 1.0 / (v ** 2)
    #return 1.0 / v
    return n.cpus / v
    #return n.cpus / v * 4 if n.arch == "amd64" else n.cpus / v


class AdaptiveWeightStrategy(WeightStrategy):

    def __init__(self):
        super().__init__()
        self.avgs = defaultdict(MovingAverage)
    
    def refresh_nodes(self, new_nodes, busy=False):
        #tmp = []

        for n in new_nodes:
            n.score_raw = time_to_weight(n, self.avgs[n.ip].read())
            #tmp.append(n.ip + ":" + str(n.score_raw))
        
        self.refresh_scores(new_nodes)
        self.nodes = new_nodes

    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        avg = self.avgs[node.ip]

        start_time = time.monotonic()
        response = self.forward_to(node, pod)
        ellapsed_time = time.monotonic() - start_time

        avg.write(ellapsed_time)
        node.score_raw = time_to_weight(node, avg.read())
        self.refresh_scores(self.nodes)
        
        return response
