from strategies.base_strategy import BaseStrategy, BaseSync

import random


class RandomStrategy(BaseStrategy):

    def __init__(self):
        super().__init__()

    def pick_node_and_pod(self):
        nodes_list = self.nodes
        node       = random.choice(nodes_list)
        pod        = random.choice(node.pods)
        return node, pod
