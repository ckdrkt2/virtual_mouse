import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pandas as pd

wCam, hCam = 640, 480
frameR = 150     #Frame Reduction
smoothening = 7  #random value

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

class stack():

    def __init__(self):
        self.stack = []
        self.length = 0

    def add(self, n):
        self.stack.append(n)
        self.length += 1
        if self.length > 10:
            self.stack.pop(0)
            self.length -= 1
    
    def variance(self):
        if self.length == 10:
            return np.var(self.stack)
        else:
            return 0

    def clear(self):
        self.stack = []
        self.length = 0

x_cor, y_cor = stack(), stack()
x_stack = stack()
y_stack = stack()
s = time.time()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1, z1 = lmList[0][1:]
        x2, y2, z2 = lmList[8][1:]

        x_cor.add(x1)
        y_cor.add(y1)
        x_stack.add(x2)
        y_stack.add(y2)

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        print(x_stack.variance(), y_stack.variance())

        if fingers[1] == 1 and sum(fingers) == 1:

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        
            if y_stack.variance() > 80 and x_cor.variance() < 30 and y_cor.variance() < 30:
                autopy.mouse.click()
                x_stack.clear()
                y_stack.clear()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
    # cv2.putText(img, str(int(x_stack.variance())), (580, 58), cv2.FONT_HERSHEY_PLAIN, 2, (8, 8, 255), 3)
    # cv2.putText(img, str(int(y_stack.variance())), (580, 108), cv2.FONT_HERSHEY_PLAIN, 2, (8, 8, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

# b = pd.DataFrame(a)
# b.to_csv("test.csv")
