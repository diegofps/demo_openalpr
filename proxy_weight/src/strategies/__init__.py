from strategies.adaptive_weight_on_busy_strategy import AdaptiveWeightOnBusyStrategy
from strategies.weight_on_busy_strategy import WeightOnBusyStrategy
from strategies.weight_strategy import WeightStrategy
from strategies.random_strategy import RandomStrategy
from strategies.min_strategy import MinStrategy

import params


def start():
    if params.MODE == "RANDOM":
        return RandomStrategy()
    
    elif params.MODE == "WEIGHT":
        return WeightStrategy()
    
    elif params.MODE == "WEIGHT_ON_BUSY":
        return WeightOnBusyStrategy()
    
    elif params.MODE == "ADAPTIVE_WEIGHT_ON_BUSY":
        return AdaptiveWeightOnBusyStrategy()
    
    elif params.MODE == "MIN":
        return MinStrategy()
    
    else:
        print("Unknown strategy mode:", params.MODE, ", using default strategy (RANDOM)")
        return RandomStrategy()
