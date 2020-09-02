from ctypes import *

import numpy as np


flib = CDLL("./libpyfacedetection.so")

_facedetect_cnn = flib.py_facedetect_cnn
_facedetect_cnn.restype = None
_facedetect_cnn.argtypes = [c_void_p, c_int, c_int, c_void_p]


class FaceDetectionCNN:

    def __init__(self):
        self.buffer = np.zeros(0x20000, np.int32)
    
    def read(self, img):
        ptr=img.ctypes.data
        rows,cols,_=img.shape
        output = self.buffer.ctypes.data
        _facedetect_cnn(ptr, cols, rows, output)

    def result_raw(self):
        return self.buffer
    
    def result(self):
        result = []
        eltos = self.buffer[0]
        p = 1

        for _ in range(eltos):
            face = {
                "confidence": int(self.buffer[p+0]),
                "rect": (int(self.buffer[p+1]), int(self.buffer[p+2]), int(self.buffer[p+3]), int(self.buffer[p+4])),
                "p1": (int(self.buffer[p+5]), int(self.buffer[p+6])),
                "p2": (int(self.buffer[p+7]), int(self.buffer[p+8])),
                "p3": (int(self.buffer[p+9]), int(self.buffer[p+10])),
                "p4": (int(self.buffer[p+11]), int(self.buffer[p+12])),
                "p5": (int(self.buffer[p+13]), int(self.buffer[p+14]))
            }
            
            result.append(face)
            p += 15

        return result


