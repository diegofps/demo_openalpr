from models import Node, Pod
import sys


def debug(*args, author=None):
    if author:
        print(author, "|", *args, file=sys.stderr)
    else:
        print(*args, file=sys.stderr)
    sys.stdout.flush()

