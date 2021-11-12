import cv2
import mediapipe as mp
import time
 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
cap = cv2.VideoCapture(0)
 
pTime = 0

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
 
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
 
        results = hands.process(image)
 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[8].x * 100)
                y = int(hand_landmarks.landmark[8].y * 100)
                z = int(hand_landmarks.landmark[8].z * 100)
                dist = 0
                cv2.putText(
                    image, text='x=%d y=%d z=%d ' % (x,y,z), org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=255, thickness=3)
 
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(image, str(int(fps)), (580, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

        cv2.imshow('image', image)
        if cv2.waitKey(1) == ord('q'):
            break
 
cap.release()