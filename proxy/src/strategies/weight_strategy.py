from strategies.base_strategy import BaseStrategy, BaseSync
from utils import debug

import random
import params


class SyncWeight(BaseSync):
    
    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        for node in nodes:
            node.score_raw = node.weight
        self.listener.refresh_nodes(nodes, busy=True)


class SyncWeightOnBusy(BaseSync):
    
    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        self.refresh_cpu_stats(nodes, onlyPrimary=True)
        
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
            debug("CPU usage is high, enabling CSDs (CPU:", avgCpu, ", Nodes:", len(nodes), ")")

            for node in nodes:
                node.score_raw = node.weight

            self.listener.refresh_nodes(nodes, busy=True)
        
        else:
            debug("CPU usage is low, using only primary nodes (CPU:", avgCpu, ", Nodes:", len(nodes), ")")
            
            for node in nodes:
                if node.primary:
                    node.score_raw = node.weight
                else:
                    node.score_raw = 0.0
            
            self.listener.refresh_nodes(nodes, busy=False)


class WeightStrategy(BaseStrategy):

    def __init__(self, sync=None):
        if sync is None:
            sync = SyncWeightOnBusy() if params.ON_BUSY else SyncWeight()
        super().__init__(sync)
    
    def refresh_nodes(self, new_nodes, busy=False):
        self.refresh_scores(new_nodes)
        self.nodes = new_nodes

    def pick_node_and_pod(self):
        nodes_list = self.nodes
        
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
        
        debug("Chose node", node.name, node.ip, "and pod", pod.name, pod.ip)
        return node, pod
