from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *                  # 드론 라이브러리
from turtle import *

import cv2
import mediapipe as mp
import time
import math

currentHeight = 0.
currentYaw = 0.

def searchPort():               # 포트 검색 함수    
    nodes = comports()
    count = 0
    for node in nodes:
        print('[{0}]'.format(count))
        print('device           : ', node.device)
        print('description      : ', node.description)
        print('manufacturer     : ', node.manufacturer)
        print('hwid             : ', node.hwid)
        print('interface        : ', node.interface)
        print('location         : ', node.location)
        print('name             : ', node.name)
        
    return node.name

def eventButton(button):        # 버튼 입력 정보 함수
    print(button.button)

def eventJoystick(joystick):    # 조이스틱 입력 정보 함수
    print(joystick.left.x, joystick.left.y, joystick.right.x, joystick.right.y)

def eventMotion(motion):        # 모션 정보 함수
    print("eventMotion()")
    print("Accel    :   {0:5},  {1:5},  {2:5}",format(motion.accelX,motion.accelY,motion.accelZ))
    print("Gyro     :   {0:5},  {1:5},  {2:5}",format(motion.gyroRoll,motion.gyroPitch,motion.gyroYaw))
    print("Angle    :   {0:5},  {1:5},  {2:5}",format(motion.angleRoll,motion.anglePitch,motion.angleYaw))

def randomLight(drone):         # 랜덤 LED 컨트롤 함수
    for i in range(0,10,1):
        r = int(random.randint(0, 255))
        g = int(random.randint(0, 255))
        b = int(random.randint(0, 255))

        dataArray = drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, r, g, b)

        sleep(2)

def takeOff(drone):             # 이륙 함수
    drone.sendTakeOff()
    sleep(0.1)
    drone.sendTakeOff()
    sleep(0.1)

def landing(drone):             # 착륙 함수
    drone.sendLanding()
    sleep(0.1)
    drone.sendLanding()
    sleep(0.1)

def readEvent(drone):           # 버튼, 조이스틱 이벤트를 할당하는 함수
    drone.setEventHandler(DataType.Button, eventButton)     # 버튼 이벤트와 연결할 함수를 지정
    drone.setEventHandler(DataType.Joystick, joystickGoto)  # 조이스틱 이벤트와 연결할 함수를 지정
    drone.setEventHandler(DataType.Motion, eventMotion)
    drone.sendPing(DeviceType.Controller)

    while True:
        drone.sendRequest(DeviceType.Drone,DataType.Motion)
        sleep(1)
        if KeyboardInterrupt:
            break;

def eventTrim(trim):            # 현재 trim의 점보를 확인하는 함수
    print("{0}, {1}, {2}, {3}".format(trim.roll,trim.pitch,trim.yaw,trim.throttle))

def setTrim(drone):             # trim을 세팅하는 함수
    drone.setEventHandler(DataType.Trim,eventTrim)

    drone.sendTrim(0,0,0,0)
    sleep(0.1)

    drone.sendRequest(DeviceType.Drone,DataType.Trim)
    sleep(0.1)
    drone.sendRequest(DeviceType.Drone,DataType.Trim)

def eventAltitude(altitude):
    print("eventAltitude()")
    # print("- Temperature: {0:.3f}".format(altitude.temperature))
    # print("- Pressure: {0:.3f}".format(altitude.pressure))
    # print("- Altitude : {0:.3f}".format(altitude.altitude))
    print("- Height : {0:.3f}".format(altitude.rangeHeight))
    global currentHeight 
    currentHeight = altitude.rangeHeight

def eventAttitude(attitude):
    print("eventAttitude()")
    # print("- roll: {0:.3f}".format(attitude.roll))
    # print("- pitch: {0:.3f}".format(attitude.pitch))
    print("- Yaw : {0:.3f}".format(attitude.yaw))
    global currentYaw 
    currentYaw = attitude.yaw

def setEvent(drone):
    drone.setEventHandler(DataType.Altitude, eventAltitude)
    drone.setEventHandler(DataType.Attitude, eventAttitude)

def maintainHeight(drone, goalHeight):
    while True:
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        sleep(0.1)
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        print(currentHeight)
        if goalHeight - 0.1 > currentHeight:
            drone.sendControlWhile(0,0,0,20,10)
        elif goalHeight + 0.1 < currentHeight:
            drone.sendControlWhile(0,0,0,-20,10)
        else:
            break
    sleep(0.1)
    drone.sendControlWhile(0,0,0,0,1)
    sleep(0.1)

def maintainYaw(drone, changeYaw):
    drone.sendRequest(DeviceType.Drone, DataType.Attitude)
    sleep(0.1)
    drone.sendRequest(DeviceType.Drone, DataType.Attitude)

    goalYaw = currentYaw + changeYaw
    if goalYaw >= 180:
        goalYaw -= 360
    elif goalYaw < -180:
        goalYaw += 360

    flag = True
    if changeYaw < 0:
        flag = False

    if flag == True:    # 왼쪽으로 움직일 때
        while True:
            drone.sendRequest(DeviceType.Drone, DataType.Attitude)
            sleep(0.1)
            drone.sendRequest(DeviceType.Drone, DataType.Attitude)
            print(goalYaw , ' ' ,currentYaw)
            if goalYaw - 15 > currentYaw:
                drone.sendControlWhile(0,0,20,0,1)
            else:
                break

    elif flag == False: # 오른쪽으로 움직일 때
        while True:
            drone.sendRequest(DeviceType.Drone, DataType.Attitude)
            sleep(0.1)
            drone.sendRequest(DeviceType.Drone, DataType.Attitude)
            print(goalYaw , ' ' ,currentYaw)
            if goalYaw + 15 < currentYaw:
                drone.sendControlWhile(0,0,-20,0,1)
            else:
                break

    sleep(0.1)
    drone.sendControlWhile(0,0,0,0,1)
    sleep(0.1)

def actionPosition(drone, x, y, z, speed, heading, rotation):
    result1, result2 = 0,0
    result1 += abs(x/(speed+0.01))
    result1 += abs(y/(speed+0.01))
    result1 += abs(z/(speed+0.01))
    result2 += abs(heading/(rotation+0.01))

    drone.sendControlPosition(x, y, z, speed, heading, rotation)
    sleep(0.01)
    drone.sendControlPosition(x, y, z, speed, heading, rotation)
    sleep(0.01)
    drone.sendControlPosition(x, y, z, speed, heading, rotation)
    sleep(0.01)
    drone.sendControlPosition(x, y, z, speed, heading, rotation)
    sleep(0.01)
    drone.sendControlPosition(x, y, z, speed, heading, rotation)
    sleep(max(result1,result2))

#사각형
def square(drone):
    print("Sqaure")
    print('')
    for i in range(0,4):
        print('각도 전환')
        actionPosition(drone,0,0,0,0,-90,45)
        #정지
        drone.sendControlWhile(0,0,0,0,1000)
        sleep(0.1)
        print('사각형 전진')
        actionPosition(drone,1,0,0,0.5,0,0)

#zigzag
def zigzag(drone):
    actionPosition(drone,0,0,0,0,-45,90)
    actionPosition(drone,0.6,0,0,0.4,0,0)
    
    actionPosition(drone,0,0,0,0,45,90)
    actionPosition(drone,0.6,0,0,0.4,0,0)
    
    actionPosition(drone,0,0,0,0,-45,90)
    actionPosition(drone,0.6,0,0,0.4,0,0)
    
    actionPosition(drone,0,0,0,0,45,90)
    actionPosition(drone,0.6,0,0,0.4,0,0)

# 기능 1 
def GO_1( drone):
    global currentHeight

    #1.호버링 3초
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 3000)
    sleep(0.1)

    #2. 전진 비행(80cm)
    print("Go")
    actionPosition(drone,0.8,0,0,0.5,0,0)

    #3. 고도상승(높이 1.5cm)
    print("Up")
    maintainHeight(drone,1.5)

    #4. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)
    sleep(0.1)
    
    #4. 사각형 패턴비행(90도 회전, 정지 1sec, 지름 1m 씩)
    square(drone)

    #5. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)
    sleep(0.1)

    #6. 원 패턴 비행(지름 1m)    
    print("Circle")
    actionPosition(drone,3.14,0,0,0.785,360,90)

    #7. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)
    sleep(0.1)

    #8. 후진 비행(1m)
    print("Back")
    actionPosition(drone,-1,0,0,0.5,0,0)
    sleep(0.1)

    #9. 고도 하강(1m 남김)
    print("Down")
    maintainHeight(drone,1)

    #10. 정지 비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)
    sleep(0.1)

# 기능 2
def GO_2( drone):
    #1.호버링 3초
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 3000)
    sleep(0.1)

    #2. 전진 비행(80cm)
    print("Go")
    actionPosition(drone,0.8,0,0,0.5,0,0)

    #3. 고도상승(높이 1.5cm)
    print("Up")
    maintainHeight(drone,1.5)

    #4. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)
    sleep(0.1)

    #5. 8자 원비행(각 원지름 1m)
    print("Circle8")
    actionPosition(drone,3.14,0,0,0.785,360,90)
    actionPosition(drone,3.14,0,0,0.785,-360,90)

    #6. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    #7. 지그재그 비행 4회(45도 방향으로 0.5sec, 전진 1.5sec)
    print("ZigZag")
    zigzag(drone)

    #8. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    #9. 전진 비행(60cm)
    print("Go")
    actionPosition(drone,0.6,0,0,0.6,0,0)

    #10. 고도 하강(높이 50cm)
    print("Down")
    maintainHeight(drone,0.5)

    #11. 정지 비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    #12. 고도 상승(높이 1m)
    print("Up")
    maintainHeight(drone,1.0)

    #13. 전진 비행(50cm)
    print("Go")
    actionPosition(drone,0.5,0,0,0.5,0,0)

    #11. 정지 비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

# 기능 3
def GO_3(drone):        
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
    fingers.append([])  # 엄지
    fingers.append([])  # 검지
    fingers.append([])  # 중지
    fingers.append([])  # 약지
    fingers.append([])  # 소지
    fingers.append([])  # 검지 밑
    fingers.append([])  # 중지 밑
    fingers.append([])  # 약지 밑
    fingers.append([])  # 소지 밑
    fingers.append([])  # 손바닥 밑
    distance = [1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0]

    degree_1 = 0.05     # 움직일 거리(float)
    speed_1 = 0.5       # 속도(float)
    degree_2 = 5        # 움직일 회전각(int)
    speed_2 = 45        # 각속도(int)

    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            handLm = results.multi_hand_landmarks[0]  
            for id, lm in enumerate(handLm.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                if id ==4:      # 엄지
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[0] = [lm.x, lm.y]
                elif id ==8:    # 검지
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[1] = [lm.x, lm.y]
                elif id ==12:   # 중지
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[2] = [lm.x, lm.y]
                elif id ==16:   # 약지
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[3] = [lm.x, lm.y]
                elif id ==20:   # 소지
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[4] = [lm.x, lm.y]

                elif id ==5:    # 검지 시작부분
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[5] = [lm.x, lm.y]
                elif id ==9:    # 중지 시작부분
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[6] = [lm.x, lm.y]
                elif id ==13:   # 약지 시작부분
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[7] = [lm.x, lm.y]
                elif id ==17:   # 소지 시작부분
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[8] = [lm.x, lm.y]
                elif id ==0:    # 손바닥 밑
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)
                    fingers[9] = [lm.x, lm.y]

            mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)

            # 인접 확인
            distance[0] = math.sqrt((fingers[0][0] - fingers[1][0]) ** 2 + (fingers[0][1] - fingers[1][1]) ** 2)    # 검지와 거리
            distance[1] = math.sqrt(((fingers[0][0] - fingers[2][0]) ** 2 + (fingers[0][1] - fingers[2][1]) ** 2))  # 중지와 거리
            distance[2] = math.sqrt(((fingers[0][0] - fingers[3][0]) ** 2 + (fingers[0][1] - fingers[3][1]) ** 2))  # 약지와 거리
            distance[3] = math.sqrt(((fingers[0][0] - fingers[4][0]) ** 2 + (fingers[0][1] - fingers[4][1]) ** 2))  # 소지와 거리

            distance[4] = math.sqrt(((fingers[0][0] - fingers[5][0]) ** 2 + (fingers[0][1] - fingers[5][1]) ** 2))  # 검지 밑과 거리
            distance[5] = math.sqrt(((fingers[0][0] - fingers[6][0]) ** 2 + (fingers[0][1] - fingers[6][1]) ** 2))  # 중지 밑과 거리
            distance[6] = math.sqrt(((fingers[0][0] - fingers[7][0]) ** 2 + (fingers[0][1] - fingers[7][1]) ** 2))  # 약지 밑과 거리
            distance[7] = math.sqrt(((fingers[0][0] - fingers[8][0]) ** 2 + (fingers[0][1] - fingers[8][1]) ** 2))  # 소지 밑과 거리

            if distance[3] < 0.07:      # Yaw Down
                print('4')
                drone.sendControlPosition(0,0,0,0,-degree_2,speed_2)
            elif distance[2] < 0.07:    # Yaw Up
                print('3')
                drone.sendControlPosition(0,0,0,0,degree_2,speed_2)
            elif distance[1] < 0.07:    # Throttle Down
                print('2')
                drone.sendControlPosition(0,0,-degree_1,speed_1,0,0)
            elif distance[0] < 0.07:    # Throttle Up
                print('1')
                drone.sendControlPosition(0,0,degree_1,speed_1,0,0)
                
            elif distance[7] < 0.03:    # Roll Up
                print('8')
                drone.sendControlPosition(0,degree_1,0,speed_1,0,0)
            elif distance[6] < 0.03:    # Roll Down
                print('7')
                drone.sendControlPosition(0,-degree_1,0,speed_1,0,0)
            elif distance[5] < 0.03:    # Pitch Down
                print('6')
                drone.sendControlPosition(-degree_1,0,0,speed_1,0,0)
            elif distance[4] < 0.03:    # Pitch Up
                print('5')
                drone.sendControlPosition(degree_1,0,0,speed_1,0,0)

            elif fingers[0][0] > fingers[4][0]: # Lending (손을 아래로 뒤집을 경우)
                print('Circle8')
                actionPosition(drone,3.14,0,0,0.785,360,90)
                actionPosition(drone,3.14,0,0,0.785,-360,90)
            elif fingers[9][1] < fingers[2][1]: # Lending (손을 아래로 뒤집을 경우)
                break        

            sleep(0.01)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
