import numpy as np
import cv2 as cv
import math

class Draw:
    def __init__(self):
        self
        self.drawing = False # true if mouse is pressed
        self.mode = 0 # if True, draw rectangle. Press 'm' to toggle to curve
        self.ix,self.iy = -1,-1 #initial positions
        self.lastx, self.lasty = 0, 0 #last x and y positions
        self.img = np.zeros((256, 256,3), np.uint8)
        self.scale_percent = 0.1
        self.settingsImg = np.zeros((200, 450, 3), np.uint8)
        self.rgb = [0, 0, 0]
        self.prevImgs = []
        self.t = 5
        
    def changeR(self, position):
        self.rgb[2] = position

    def changeG(self, position):
        self.rgb[1] = position

    def changeB(self, position):
        self.rgb[0] = position

    def changeT(self, position):
        self.t = position

    #Finds what x and y directions the mouse is moving in, returning an array of directions
    def findDirection(self, ix, iy, x, y):
        directions = []
        if x > ix:
            directions.append(1)
        elif x == ix:
            directions.append(0)
        else:
            directions.append(-1)
        if y > iy:
            directions.append(1)
        elif y == iy:
            directions.append(0)
        else:
            directions.append(-1)
        return directions

    def resetCanvas(self):
        self.img.fill(0)
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self.img,'m, r, esc, u, s',(10,500), font, 0.8,(255,255,255),2,cv.LINE_AA)

    def draw_rect(self, x, y):
        rectangleDirection = self.findDirection(self.ix, self.iy, x, y)
        a = self.ix + self.t * rectangleDirection[0]
        b = self.iy + self.t * rectangleDirection[1]
        c = x - self.t * rectangleDirection[0]
        d = y - self.t * rectangleDirection[1]
        cv.rectangle(self.img,(self.ix,self.iy),(a,y),self.rgb,-1)
        cv.rectangle(self.img,(c,self.iy),(x,y),self.rgb,-1)
        cv.rectangle(self.img,(self.ix,d),(x,y),self.rgb,-1)
        cv.rectangle(self.img,(self.ix,self.iy),(x,b),self.rgb,-1)

    def draw_line(self, x, y):
        cv.line(self.img,(self.lastx, self.lasty),(x, y),self.rgb,self.t)

    def draw_circle(self, x, y):
        radius = max(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2), 5)
        cv.circle(self.img, (self.ix, self.iy), int(radius), self.rgb, self.t)

    def checkSame(self, newPixels, pixel, originalColor, color):
        if np.all(self.img[pixel[0], pixel[1]] == originalColor):
            self.img[pixel[0], pixel[1]] = color
            newPixels.add(pixel)

    def draw_fill(self, x, y):
        originalColor = np.copy(self.img[y, x])
        self.img[y, x] = self.rgb
        if np.all(originalColor == self.rgb):
            return -1

        pixels = set()
        originalCoords = (y, x)
        pixels.add(originalCoords)
        i = 0
        while len(pixels) > 0 and i < 50000:
            cv.waitKey(1)
            cv.imshow('image', self.img)
            newPixels = set()
            for pixel in pixels:
                if (pixel[0] != 0):
                    self.checkSame(newPixels, (pixel[0] - 1, pixel[1]), originalColor, self.rgb)
                if (pixel[0] != len(self.img) - 1):
                    self.checkSame(newPixels, (pixel[0] + 1, pixel[1]), originalColor, self.rgb)
                if (pixel[1] != 0):
                    self.checkSame(newPixels, (pixel[0], pixel[1] - 1), originalColor, self.rgb)
                if (pixel[1] != len(self.img[0]) - 1):
                    self.checkSame(newPixels, (pixel[0], pixel[1] + 1), originalColor, self.rgb)
            pixels = newPixels
            i += len(pixels)

    def draw_settings(self):
        self.settingsImg.fill(0)
        if self.mode == 0:
            cv.line(self.settingsImg, (10, 100), (440, 100), self.rgb, self.t)
        elif self.mode == 1:
            cv.rectangle(self.settingsImg, (125, 10), (325, 190), self.rgb, self.t)
            cv.rectangle(self.settingsImg, (125 + self.t, 10 + self.t), (325 - self.t, 190 - self.t), (0, 0, 0), self.t)
        elif self.mode == 2:
            cv.circle(self.settingsImg, (225, 100), 50, self.rgb, self.t)
        elif self.mode == 3:
            self.settingsImg[:] = self.rgb