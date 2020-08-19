from strategies.base_strategy import BaseStrategy, BaseSync
from strategies.weight_strategy import WeightStrategy

import random
import params


class WeightOnBusyStrategy(WeightStrategy):

    def __init__(self):
        super().__init__(SyncWeightOnBusy())


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
            print("Warning: No primary node detected")
            avgCpu = 1.0
            
        else:
            avgCpu = sumCpu / numCpu
        
        # Update the scores
        if avgCpu >= params.MIN_CPU_FOR_WEIGHT:
            print("CPU usage is high, enabling CSDs (CPU:", avgCpu, ", Nodes:", len(nodes), ")")

            for node in nodes:
                node.score_raw = node.weight

            self.listener.refresh_nodes(nodes, busy=True)
        
        else:
            print("CPU usage is low, using only primary nodes (CPU:", avgCpu, ", Nodes:", len(nodes), ")")
            
            for node in nodes:
                if node.primary:
                    node.score_raw = node.weight
                else:
                    node.score_raw = 0.0
            
            self.listener.refresh_nodes(nodes, busy=False)
