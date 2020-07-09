from flask import json, jsonify, app, Flask, request
from openalpr import Alpr
import sys

## Init web server app

app = Flask(__name__)

## Init openalpr

alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")

## Routes

@app.route('/summary', methods=["GET"])
def summary():
    return jsonify(name="Diego", surname="Souza")

@app.route('/image', methods=["POST"])
def image():
    try:
        imagefile = request.files.get('imagefile', '')
        data = imagefile.stream.read()
        results = alpr.recognize_array(data)
        #import pdb; pdb.set_trace()
        return jsonify(result="ok", data=results)
    except Exception as err:
        print(err)
        return jsonify(result="sorry :/")


