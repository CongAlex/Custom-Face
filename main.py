import numpy as np
import cv2 as cv
import draw 

myDraw = draw.Draw()

# mouse callback function
# Either draws hollow rectangles or circles depending on mode, which is toggled by pressing "m"
# Circles radius changes depending on mouse move speed

def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        myDraw.drawing = True
        myDraw.ix,myDraw.iy = x,y
        myDraw.lastx, myDraw.lasty = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if myDraw.drawing == True:
            if myDraw.mode == 0:
                myDraw.draw_line(x, y)
            elif myDraw.mode == 1:
                myDraw.img = myDraw.prevImgs[-1].copy()
                myDraw.draw_rect(x, y)
            elif myDraw.mode == 2:
                myDraw.img = myDraw.prevImgs[-1].copy()
                myDraw.draw_circle(x, y)
        myDraw.lastx, myDraw.lasty = x, y
    
    elif event == cv.EVENT_LBUTTONUP:
        myDraw.drawing = False
        if myDraw.mode == 0:
            myDraw.draw_line(x, y)
        elif myDraw.mode == 1:
            myDraw.img = myDraw.prevImgs[-1].copy()
            myDraw.draw_rect(x, y)
        elif myDraw.mode == 2:
            myDraw.draw_circle(x, y)
        elif myDraw.mode == 3:
            myDraw.draw_fill(x, y)
        myDraw.prevImgs.append(myDraw.img.copy())

myDraw.resetCanvas()
myDraw.prevImgs.append(myDraw.img.copy())
cv.namedWindow('image')
cv.setMouseCallback('image', on_mouse)
cv.namedWindow('settings')

cv.createTrackbar('R', 'settings', 255, 255, myDraw.changeR)
cv.createTrackbar('G', 'settings', 255, 255, myDraw.changeG)
cv.createTrackbar('B', 'settings', 255, 255, myDraw.changeB)
cv.createTrackbar('thickness', 'settings', 5, 30, myDraw.changeT)

while(1):
    cv.imshow('image',myDraw.img)
    k = cv.waitKey(5) & 0xFF
    if k == ord('m'):
        myDraw.mode += 1
        myDraw.mode %= 4
    if k == ord('r'): #Press "r" to reset canvas
        myDraw.drawInstance.resetCanvas()
        myDraw.prevImgs.append(myDraw.img.copy())
    elif k == ord('u'): #press "u" to undo
        if len(myDraw.prevImgs) > 1:
            myDraw.prevImgs.pop()
            myDraw.img = myDraw.prevImgs[-1].copy()
    elif k == ord("s"):
        cv.imwrite("test/drawing.png", myDraw.img)
    elif k == 27: #Press esc to escape
        break
    
    cv.imshow('settings', myDraw.settingsImg)
    myDraw.draw_settings()
 
cv.destroyAllWindows()