import sys


def debug(*args, author=None):
    if author:
        print(author, "|", *args, file=sys.stderr)
    else:
        print(*args, file=sys.stderr)
    sys.stdout.flush()


def read_data(data, path, default_value=None):
    current = data

    for key in path:
        if not key in current:
            print("missing key", key, "in path", path)
            return default_value
        else:
            current = current[key]
    
    return current
