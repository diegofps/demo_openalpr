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
    