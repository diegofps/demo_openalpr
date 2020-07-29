#!/usr/bin/python3

from flask import jsonify, Flask, request, Response
import requests


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
target = 'http://localhost:4568/'
app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def _proxy(path):
    #print("path=", path)
    #print("args=", str(request.args))
    #print("url=", request.url)
    #print("host_url=", request.host_url)
    #print("url2=", request.url.replace(request.host_url, 'https://wespa.com.br/'))
    
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, target),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    #body = resp.content
    body = resp.iter_content(chunk_size=10*1024)
    
    response = Response(body, resp.status_code, headers)
    
    return response

