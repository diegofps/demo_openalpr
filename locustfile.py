import random
from locust import HttpUser, task, between
from glob import glob

class OpenALPRUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def recognize(self):
        r = self.client.post("/recognize", files={'imagefile': self.filedata})
        print(r.status_code, r.text)
    
    def on_start(self):
        self.filepaths = glob("./dataset/*")
        self.filepath = "/home/diego/Sources/openalpr/image_0001.jpg"
        with open(self.filepath, "rb") as fin:
            self.filedata = fin.read()
        # self.client.post("/login", {"username":"foo", "password":"bar"})
        pass

