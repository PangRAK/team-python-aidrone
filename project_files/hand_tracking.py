from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들

import cv2
import mediapipe as mp
import time
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

fingers = []
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
fingers.append([])
distance = [1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0]

searchPort() # 포트 찾기

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        handLm = results.multi_hand_landmarks[0]  
        for id, lm in enumerate(handLm.landmark):
            # print(id,'  ' ,lm.x)
            # print(type(id),'  ' ,type(lm.x))
            # sleep(10)
            #print(id,lm)
            h, w, c = img.shape
            cx, cy = int(lm.x *w), int(lm.y*h)
            if id ==4: # 엄지
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[0] = [lm.x, lm.y]
            elif id ==8: # 검지
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[1] = [lm.x, lm.y]
            elif id ==12: # 중지
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[2] = [lm.x, lm.y]
            elif id ==16: # 약지
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[3] = [lm.x, lm.y]
            elif id ==20: # 소지
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[4] = [lm.x, lm.y]

            elif id ==5: # 검지 시작부분
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[5] = [lm.x, lm.y]
            elif id ==9: # 중지 시작부분
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[6] = [lm.x, lm.y]
            elif id ==13: # 약지 시작부분
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[7] = [lm.x, lm.y]
            elif id ==17: # 소지 시작부분
                cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                fingers[8] = [lm.x, lm.y]

        mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)

        # 인접 확인
        distance[0] = math.sqrt((fingers[0][0] - fingers[1][0]) ** 2 + (fingers[0][1] - fingers[1][1]) ** 2)
        distance[1] = math.sqrt(((fingers[0][0] - fingers[2][0]) ** 2 + (fingers[0][1] - fingers[2][1]) ** 2))
        distance[2] = math.sqrt(((fingers[0][0] - fingers[3][0]) ** 2 + (fingers[0][1] - fingers[3][1]) ** 2))
        distance[3] = math.sqrt(((fingers[0][0] - fingers[4][0]) ** 2 + (fingers[0][1] - fingers[4][1]) ** 2))

        distance[4] = math.sqrt(((fingers[0][0] - fingers[5][0]) ** 2 + (fingers[0][1] - fingers[5][1]) ** 2))
        distance[5] = math.sqrt(((fingers[0][0] - fingers[6][0]) ** 2 + (fingers[0][1] - fingers[6][1]) ** 2))
        distance[6] = math.sqrt(((fingers[0][0] - fingers[7][0]) ** 2 + (fingers[0][1] - fingers[7][1]) ** 2))
        distance[7] = math.sqrt(((fingers[0][0] - fingers[8][0]) ** 2 + (fingers[0][1] - fingers[8][1]) ** 2))

        if distance[3] < 0.07:      # Yaw Down
            print('4')
        elif distance[2] < 0.07:    # Yaw Up
            print('3')
        elif distance[1] < 0.07:    # Throttle Down
            print('2')
        elif distance[0] < 0.07:    # Throttle Up
            print('1')
            
        elif distance[7] < 0.03:    # Roll Down
            print('8')
        elif distance[6] < 0.03:    # Roll Up
            print('7')
        elif distance[5] < 0.03:    # Pitch Down
            print('6')
        elif distance[4] < 0.03:    # Pitch Up
            print('5')

        


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)