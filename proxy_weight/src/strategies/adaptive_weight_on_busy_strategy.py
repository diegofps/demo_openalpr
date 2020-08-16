from strategies.weight_on_busy_strategy import WeightOnBusyStrategy
from collections import defaultdict
from utils import MovingAverage

import time

def time_to_weight(v):
    return 1.0 / (v ** 2)


class AdaptiveWeightOnBusyStrategy(WeightOnBusyStrategy):

    def __init__(self):
        super().__init__()
        self.avgs = defaultdict(MovingAverage)
    
    def refresh_nodes(self, new_nodes, busy=False):
        if busy:
            tmp = []

            for n in new_nodes:
                n.score_raw = time_to_weight(self.avgs[n.ip].read())
                tmp.append(n.ip + ":" + str(n.score_raw))
                
            print("Server is busy, applying Adaptive Weight: ", " ".join(tmp))
            
        else:
            print("This server is not busy")
        
        self.refresh_scores(new_nodes)
        self.nodes = new_nodes

    def forward(self, path):
        node, pod = self.pick_node_and_pod()
        avg = self.avgs[node.ip]

        start_time = time.monotonic()
        response = self.forward_to(node, pod)
        ellapsed_time = time.monotonic() - start_time

        avg.write(ellapsed_time)
        node.score_raw = time_to_weight(avg.read())
        self.refresh_scores(self.nodes)
        
        return response
