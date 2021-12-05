import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import matplotlib.pyplot as plt

wCam, hCam = 640, 480
frameR = 100     #Frame Reduction
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

    def __init__(self, max_length):
        self.max_length = max_length
        self.stack = []
        self.length = 0

    def add(self, n):
        self.stack.append(n)
        self.length += 1
        if self.length > self.max_length:
            self.stack.pop(0)
            self.length -= 1
    
    def variance(self):
        if self.length == self.max_length:
            return np.var(self.stack)
        else:
            return 0

    def average(self):
        if self.length > 0:
            return sum(self.stack)/self.length
        else:
            return 0

    def derivative(self):
        if self.length == self.max_length:
            return sum([self.stack[i+1] - self.stack[i] for i in range(self.length-1)])
        else:
            return 0

    def diff(self):
        if self.length == self.max_length:
            diff1 = np.diff(self.stack)
            diff2 = np.diff(diff1)
            return diff1, diff2
        else:
            return False

    def clear(self):
        self.stack = []
        self.length = 0

stack_length = 5
x_cor, y_cor = stack(stack_length), stack(stack_length)
z2 = 0
y2 = 0
y_stack = stack(stack_length)

aa,bb,cc, dd = [], [], [], []

fingers = [0, 0, 0, 0, 0]

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        x1, y1, z1 = lmList[5][1:]
        x2, y2, z2 = lmList[8][1:]

        z2 *= 100

        y_stack.add(y2)

        x_cor.add(x1)
        y_cor.add(y1)

        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        
        if fingers[1] == 1 and sum(fingers[1:]) == 1:

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            try:
                autopy.mouse.move(wScr - clocX, clocY)
                # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            except:
                print(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY 

            if x_cor.variance() < 15 and y_cor.variance() < 15:
                # if y_stack.variance() > 200:
                #     autopy.mouse.click()
                #     cv2.putText(img, 'click', (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (8, 8, 255), 3)
                if y_stack.diff() != False:
                    dif1, dif2 = y_stack.diff()
                    print(dif1, dif2)
                    if sum(dif2) < -10:
                        autopy.mouse.click()
                        cv2.putText(img, 'click', (28, 58), cv2.FONT_HERSHEY_PLAIN, 5, (8, 8, 255), 5)
                        y_stack.clear()
            
            else:
                y_stack.clear()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
    # cv2.putText(img, str(int(fingers[1])), (28, 108), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break