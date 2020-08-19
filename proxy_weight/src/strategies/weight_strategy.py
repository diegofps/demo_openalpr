from strategies.base_strategy import BaseStrategy, BaseSync

import random


class WeightStrategy(BaseStrategy):

    def __init__(self, sync=SyncWeight()):
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
        
        print("Chose node", node.name, node.ip, "and pod", pod.name, pod.ip)
        return node, pod

class SyncWeight(BaseSync):
    
    def __init__(self):
        super().__init__()
    
    def sync(self):
        nodes = self.detect_nodes_and_pods()
        for node in nodes:
            node.score_raw = node.weight
        self.listener.refresh_nodes(nodes, busy=True)
