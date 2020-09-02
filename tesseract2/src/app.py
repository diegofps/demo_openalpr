from flask import jsonify, Flask, request
from PIL import Image

import tesserwrap
import traceback
import sys
import io


# Init the tesseract
tr = tesserwrap.Tesseract(lang="por")

# Init web Server
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/recognize', methods=["POST"])
def image():
    try:
        imagefile = request.files.get('imagefile', '')
        img  = Image.open(imagefile.stream)
        text = tr.ocr_image(img)

        return jsonify(result="ok", data=text)
    except Exception as err:
        traceback.print_exc()
        print(err)
        return jsonify(result="sorry :/")


