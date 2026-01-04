import cv2 as cv
import numpy as np

class Camera:
    def __init__(self):
        self

    def updateImage(self, frame, drawImg):
        dHeight, dWidth, dChannels = drawImg.shape
        for y in range(dHeight):
            for x in range(dWidth):
                pixel = drawImg[y, x]
                if (pixel != [0, 0, 0]).all():
                    frame[y, x] = pixel

