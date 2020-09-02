from locust import HttpUser, task, between
from glob import glob

import resource
import random
import os

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

class OpenALPRUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def recognize(self):
        self.client.post("/recognize", files={'imagefile': self.filedata})
        #print(r.status_code, r.text)
    
    def on_start(self):
        #self.filepaths = glob("./datasets/openalpr/*")
        self.filepath = os.path.expanduser("~/Sources/demo_openalpr/datasets/face/hss-2019_small.jpg")
        
        with open(self.filepath, "rb") as fin:
            self.filedata = fin.read()
