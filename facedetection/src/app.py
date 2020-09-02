from pyfacedetectioncnn import FaceDetectionCNN
from flask import jsonify, Flask, request

import numpy as np

import traceback
import sys
import cv2
import io


# Init the tesseract
fc=FaceDetectionCNN()

# Init web Server
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/recognize', methods=["POST"])
def image():
    try:
        imagefile = request.files.get('imagefile', '')
        array=np.asarray(bytearray(imagefile.stream.read()), np.uint8)
        img=cv2.imdecode(array, cv2.IMREAD_COLOR)
        fc.read(img)

        return jsonify(result="ok", data=fc.result())
    except Exception as err:
        traceback.print_exc()
        print(err)
        return jsonify(result="sorry :/")


