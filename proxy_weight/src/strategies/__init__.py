from strategies.adaptive_weight_on_busy_strategy import AdaptiveWeightOnBusyStrategy
from strategies.weight_on_busy_strategy import WeightOnBusyStrategy
from strategies.weight_strategy import WeightStrategy
from strategies.random_strategy import RandomStrategy
from strategies.min_strategy import MinStrategy

import params


def start():
    if params.STRATEGY == "RANDOM":
        return RandomStrategy()
    
    elif params.STRATEGY == "WEIGHT":
        return WeightStrategy()
    
    elif params.STRATEGY == "WEIGHT_ON_BUSY":
        return WeightOnBusyStrategy()
    
    elif params.STRATEGY == "ADAPTIVE_WEIGHT_ON_BUSY":
        return AdaptiveWeightOnBusyStrategy()
    
    elif params.STRATEGY == "MIN":
        return MinStrategy()
    
    else:
        print("Unknown strategy:", params.STRATEGY, ", using default strategy (RANDOM)")
        return RandomStrategy()
