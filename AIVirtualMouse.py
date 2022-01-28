import cv2
import numpy as np
import HandTrackingModule as htm
import mystack as ms
import time
import mouse as cursor
from pynput.mouse import Button, Controller
import threading
from multiprocessing import Process 
import playsound

class untacttact:

    def __init__(self):
        wCam, hCam = 640, 480
        frameR = 100
        smoothening = 7

        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap.set(3, wCam)
        # cap.set(4, hCam)

        # detector = htm.handDetector(maxHands=1)

        mouse = Controller()

        mouse.move(9999,9999)

        wScr, hScr = mouse.position
        wScr += 1; hScr += 1

        stack_length = 5
        max_var = 10
        max_diff = -15

        x_cor, y_cor, y_stack = ms.mystack(stack_length), ms.mystack(stack_length), ms.mystack(stack_length)

        fingers = [0, 0, 0, 0, 0]

        while True:
            success, img = cap.read()
            img = detector.findHands(img, draw=True)
            lmList, bbox = detector.findPosition(img, draw=False)

            if len(lmList) != 0:

                x_y = np.array([0,0])
                for i in [1,2,3,4,9,13,17]:
                    x_y = np.add(x_y, lmList[i][1:])
                x1, y1 = x_y / 7

                y_stack.add(lmList[8][2])

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
                        cursor.move(wScr - clocX, clocY)
                        pass
                    except:
                        print(wScr - clocX, clocY)
                    plocX, plocY = clocX, clocY 
                    
                    if x_cor.var() < max_var and y_cor.var() < max_var:
                        # print('a', y_stack.stack, end=' ')
                        if y_stack.diff() < max_diff:
                            mouse.click(Button.left, 1)
                            cv2.putText(img, 'click', (458, 58), cv2.FONT_HERSHEY_PLAIN, 5, (8, 8, 255), 5)
                            y_stack.clear()
                        # else:
                        #     print()
                    else:
                        # print(y_cor.var(), '#############')
                        y_stack.clear()
                else:
                    y_stack.clear()
            
            else:
                pass
                break

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            
            cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
            # cv2.putText(img, str(int(y2)), (28, 108), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
            # cv2.putText(img, str(int(x_cor.var())), (528, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
            # cv2.putText(img, str(int(y_cor.var())), (528, 108), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
            # print(x_cor.var(), y_cor.var())

            cv2.imshow("Image", img)
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == '__main__':

    def sound():
        playsound.playsound('mooyaho.mp3')

    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    detector = htm.handDetector(maxHands=1)

    while True:
        
        success, img = cap.read()
            
        img = detector.findHands(img, draw=True)
        lmList, bbox = detector.findPosition(img, draw=False)

        if len(lmList) != 0:

            distance = int(bbox[-1]*-100)

            cv2.putText(img, str(distance), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)
            # print(bbox[2]-bbox[0], bbox[3] - bbox[1])
            if distance > 10 and (bbox[2]-bbox[0] > 100 or bbox[3] - bbox[1] > 100):

                t = threading.Thread(target=sound)
                t.start()

                untacttact()

                t.join()

                continue

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break