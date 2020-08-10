def read_data(data, path, default_value=None):
    current = data

    for key in path:
        if not key in current:
            print("missing key", key, "in path", path)
            return default_value
        else:
            current = current[key]
    
    return current
    

def is_pod_ready(item):
    if not "status" in item:
        return False
    
    if not "containerStatuses" in item["status"]:
        return False
    
    if not "podIP" in item["status"]:
        return False
    
    if not "hostIP" in item["status"]:
        return False
    
    if any(x["ready"] == False for x in item["status"]["containerStatuses"]):
        return False
    
    return True


class Node:

    def __init__(self, data):
        self.arch   = read_data(data, ["metadata", "labels", "kubernetes.io/arch"], "Unknown")
        self.ip     = read_data(data, ["metadata", "labels", "k3s.io/internal-ip"])
        self.cpus   = int(read_data(data, ["status", "capacity", "cpu"], 1))
        self.name   = read_data(data, ["metadata", "name"], "Unknown")
        self.weight = float(read_data(data, ["metadata", "labels", "weight"], self.cpus))
        # self.data   = data
        
        self.score_sum = 0.0
        self.score_raw = 0.0
        self.score     = 0.0
        self.idle      = 0.0
        self.busy      = 1.0
        self.pods      = []
        self.pod       = 0
    
    def add(self, podIP):
        self.pods.append(podIP)
    
    def __getstate__(self):
        return self.__dict__


class Pod:

    def __init__(self, data):
        self.app       = read_data(data, ["metadata", "labels", "app"], "Unknown")
        self.namespace = read_data(data, ["metadata", "namespace"], "Unknown")
        self.hostIP    = read_data(data, ["status", "hostIP"], "Unknown")
        self.name      = read_data(data, ["metadata", "name"], "Unknown")
        self.ip        = read_data(data, ["status", "podIP"], "Unknown")
        self.isReady   = is_pod_ready(data)
        # self.data      = data
