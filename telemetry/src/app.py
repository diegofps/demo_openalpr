#!/usr/bin/python3

from subprocess import Popen, PIPE, TimeoutExpired
from threading import Thread
from flask import Flask

import jsonpickle
import traceback
import random
import shlex
import json
import time
import sys
import os


REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "5"))
HOST_HOSTNAME   = os.getenv("HOST_HOSTNAME", "Unknown")


def get_telemetry():
    name = "Unknown"
    arch = "Unknown"
    idle = 0.0
    busy = 1.0
    cpus = 1
    
    cmd = "mpstat 1 1 -o JSON"
    cmd = shlex.split(cmd)
    
    with Popen(cmd, stdout=PIPE) as proc:
        try:
            stdout, _ = proc.communicate(timeout=3)
            
        except TimeoutExpired:
            proc.kill()
            stdout, _ = proc.communicate()
    
    if not stdout or b'not found' in stdout:
        print("not found")
        return name, idle, busy, arch, cpus
    
    try:
        data = json.loads(stdout)
        host = data["sysstat"]["hosts"][0]
        
        idle = host["statistics"][0]['cpu-load'][0]['idle'] / 100.
        name = HOST_HOSTNAME
        arch = host["machine"]
        cpus = host["number-of-cpus"]
        busy = 1.0 - idle
        
    except:
        print(b"CORRUPTED JSON IN RESPONSE: " + stdout)
        traceback.print_exc(file=sys.stdout)
    
    return name, idle, busy, arch, cpus


class Sync(Thread):

    def __init__(self):
        super().__init__()

    def sync(self):
        telemetry = get_telemetry()

        data = {
            "name": telemetry[0],
            "idle": telemetry[1],
            "busy": telemetry[2],
            "arch": telemetry[3],
            "cpus": telemetry[4],
        }

        global body
        body = jsonpickle.encode(data, unpicklable=False)

    def run(self):
        sleep_before = int(random.random() * REFRESH_SECONDS)
        sleep_after = REFRESH_SECONDS - sleep_before
        
        while True:
            try:
                time.sleep(sleep_before)
                print("Starting telemetry")
                self.sync()
                print("Telemetry ended")
                time.sleep(sleep_after)

            except KeyboardInterrupt:
                print("Bye")
                break
            
            except:
                traceback.print_exc(file=sys.stdout)


data = {
    "name": "Unknown",
    "idle": 0.0,
    "busy": 1.0,
    "arch": "amd64",
    "cpus": "1",
}


body = jsonpickle.encode(data, unpicklable=False)
app = Flask(__name__)
sync = Sync()
sync.start()


@app.route('/', methods=["GET"])
def get():
    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )

