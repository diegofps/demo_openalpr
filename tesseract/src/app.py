from flask import jsonify, Flask, request
from PIL import Image

import pytesseract
import traceback
import sys
import io


# Init the tesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Init web Server
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/recognize', methods=["POST"])
def image():
    try:
        imagefile = request.files.get('imagefile', '')
        img  = Image.open(imagefile.stream)
        text = pytesseract.image_to_string(img, lang="por")

        return jsonify(result="ok", data=text)
    except Exception as err:
        traceback.print_exc()
        print(err)
        return jsonify(result="sorry :/")


