from strategies.adaptive_weight_strategy import AdaptiveWeightStrategy
from strategies.weight_strategy import WeightStrategy
from strategies.random_strategy import RandomStrategy
from strategies.min_strategy import MinStrategy

import params


def start():
    if params.STRATEGY == "RANDOM":
        return RandomStrategy()
    
    elif params.STRATEGY == "WEIGHT":
        return WeightStrategy()
    
    elif params.STRATEGY == "ADAPTIVE_WEIGHT":
        return AdaptiveWeightStrategy()
    
    elif params.STRATEGY == "MIN":
        return MinStrategy()
    
    else:
        print("Unknown strategy:", params.STRATEGY, ", using default strategy (RANDOM)")
        return RandomStrategy()
