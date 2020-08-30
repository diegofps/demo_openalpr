from params import API_SERVER, CLIENT_CRT, CLIENT_KEY, SERVER_CRT, APP_NAME
from models import Node

import requests


def get_nodes():
    r = requests.get(API_SERVER + "/api/v1/nodes", 
            cert=(CLIENT_CRT, CLIENT_KEY), 
            verify=SERVER_CRT)
    
    return r.json()["items"]


def get_pods():
    r = requests.get(API_SERVER + "/api/v1/pods?labelSelector=app=" + APP_NAME, 
            cert=(CLIENT_CRT, CLIENT_KEY), 
            verify=SERVER_CRT)
    
    return r.json()["items"]

