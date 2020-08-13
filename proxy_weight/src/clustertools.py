from subprocess import Popen, PIPE, TimeoutExpired
from utils import debug

import traceback
import params
import shlex
import json
import sys


def get_stats(node_ip):
    debug("Get nodes stats")
    
    name = "Unknown"
    arch = "Unknown"
    idle = 0.0
    busy = 1.0
    cpus = 1
    
    addr = node_ip if params.SSH_USER == '' else params.SSH_USER + '@' + node_ip
    
    cmd = "ssh -o \"StrictHostKeyChecking no\" -i {} {} 'mpstat 1 1 -o JSON'".format(params.SSH_PRIVATE_KEY, addr)
    debug(cmd)
    cmd = shlex.split(cmd)
    
    with Popen(cmd, stdout=PIPE) as proc:
        try:
            stdout, _ = proc.communicate(timeout=3)
        except TimeoutExpired:
            proc.kill()
            stdout, _ = proc.communicate()
    
    if not stdout or b'not found' in stdout:
        debug("not found")
        return name, idle, busy, arch, cpus
    
    try:
        data = json.loads(stdout)
        host = data["sysstat"]["hosts"][0]
        
        idle = host["statistics"][0]['cpu-load'][0]['idle'] / 100.
        name = host["nodename"]
        arch = host["machine"]
        cpus = host["number-of-cpus"]
        busy = 1.0 - idle
        # debug("success")
    except:
        debug(b"CORRUPTED JSON IN RESPONSE: " + stdout, author=node_ip)
        traceback.print_exc(file=sys.stdout)
    
    return name, idle, busy, arch, cpus
