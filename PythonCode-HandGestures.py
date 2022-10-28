import cv2
import time
from cv2 import VideoCapture
import mediapipe as mp
import serial

ser = serial.Serial('COM8',9600)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

cap = cv2.VideoCapture(0)

pTime = 0

tipIds = [4,8,12,16,20]

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        success,image = cap.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]
        
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
                
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0) 
            
            fingerState = fingers.count(1)
            print((fingerState))
            
            if fingerState == 0:
                cv2.rectangle(image, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "0", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
                cv2.putText(image, "Stop", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
                ser.write(b'5')
                time.sleep(2) # wait for the serial connection to initialize
                
            elif fingerState == 1:
                cv2.rectangle(image, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "1", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
                cv2.putText(image, "Back", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
                ser.write(b'2')
                time.sleep(2) # wait for the serial connection to initialize
                
                
            elif fingerState == 2:
                cv2.rectangle(image, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "2", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
                cv2.putText(image, "right", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
                ser.write(b'6')
                time.sleep(2) # wait for the serial connection to initialize
            
            
            elif fingerState == 3:
                cv2.rectangle(image, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "3", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
                cv2.putText(image, "left", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
                ser.write(b'4')
                time.sleep(2) # wait for the serial connection to initialize
                
                
            elif fingerState == 5:
                cv2.rectangle(image, (20, 225), (170, 460), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "5", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 255, 255), 25)
                cv2.putText(image, "Front", (52, 425), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 255), 3)
                ser.write(b'8')
                time.sleep(2) # wait for the serial connection to initialize
            
            
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
            
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k==ord('q'):
            break
    
VideoCapture.release()
cv2.destroyAllWindows()
