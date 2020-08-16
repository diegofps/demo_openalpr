import params
import sys


def debug(*args, author=None):
    if author:
        print(author, "|", *args, file=sys.stderr)
    else:
        print(*args, file=sys.stderr)
    sys.stdout.flush()


def read_data(data, path, default_value=None, warnOnMiss=True):
    current = data

    for key in path:
        if key in current:
            current = current[key]

        elif warnOnMiss:
            print("missing key", key, "in path", path)
            return default_value
            
        else:
            return default_value
    
    return current


def read_bool(data):
    if data is None:
        return False
    
    data = data[0]

    if data == 't' or data == 'T':
        return True
    
    if data == 'y' or data == 'Y':
        return True
    
    if data == '1':
        return True
    
    return False


class MovingAverage:

    def __init__(self):
        self.values = [1 for _ in range(params.MOVING_AVERAGE_LEN)]
        self.current = sum(self.values)
        self.p = 0
    
    def write(self, value):
        value = int(value * 1000)
        self.current += value - self.values[self.p]
        self.values[self.p] = value
        self.p += 1

        if self.p == params.MOVING_AVERAGE_LEN:
            self.p = 0
    
    def read(self):
        return self.current / float(params.MOVING_AVERAGE_LEN)
