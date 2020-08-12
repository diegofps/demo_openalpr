from flask import jsonify, Flask, request

import traceback
import openalpr
import sys


## Init OpenALPR
alpr = openalpr.Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")


## Init web Server
app = Flask(__name__)

@app.route('/recognize', methods=["POST"])
def image():
    try:
        imagefile = request.files.get('imagefile', '')
        data = imagefile.stream.read()
        results = alpr.recognize_array(data)
        return jsonify(result="ok", data=results)
    except Exception as err:
        traceback.print_exc()
        print(err)
        return jsonify(result="sorry :/")


