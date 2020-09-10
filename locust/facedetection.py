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
        self.filepath = os.path.expanduser("~/Sources/demo_openalpr/datasets/face/9c82c7a0-0963-4b57-a4a8-bc4a9cf5d0b0-large16x9_GettyImages1134307248.jpg")
        
        with open(self.filepath, "rb") as fin:
            self.filedata = fin.read()
