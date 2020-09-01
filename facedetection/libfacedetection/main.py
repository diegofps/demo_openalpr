#!/usr/bin/python3

from pyfacedetectioncnn import FaceDetectionCNN
import numpy as np
import cv2

with open("/home/diego/Sources/demo_openalpr/datasets/face/ey-staff-at-event.jpg.rendition.3840.2560.jpg", "rb") as fin:
    data=fin.read()

array=np.asarray(bytearray(data), np.uint8)
img=cv2.imdecode(array, cv2.IMREAD_COLOR)
#img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#ptr=img.ctypes.data
#rows,cols,depth=img.shape

fc=FaceDetectionCNN()
fc.read(img)

print(fc.result())
