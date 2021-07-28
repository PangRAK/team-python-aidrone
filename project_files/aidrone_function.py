from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *                  # 드론 라이브러리
from pynput.keyboard import Listener, Key       # 키보드 입력 감지 라이브러리
from turtle import *

currentHeight = 0.

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

def eventButton(button):        # 버튼 입력 정보 함수
    print(button.button)

def eventJoystick(joystick):    # 조이스틱 입력 정보 함수
    print(joystick.left.x, joystick.left.y, joystick.right.x, joystick.right.y)

def joystickGoto(joystick):     # 조이스틱 입력 정보 함수
    goto(joystick.right.x, joystick.right.y)

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
    print("TakeOff")
    drone.sendTakeOff()
    sleep(0.01)
    drone.sendControlWhile(0,0,0,0,5000)

def landing(drone):             # 착륙 함수
    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)


def testHovering(drone):        # 호버링 테스트 함수
    print("Hovering")
    drone.sendControlWhile(0,0,0,0,3000)

def throttleUp(drone): 
    print("Throttle Up")
    drone.sendControlWhile(0,0,0,25,2000)

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
    sleep(0.01)

    drone.sendRequest(DeviceType.Drone,DataType.Trim)
    sleep(0.01)

def testMove(drone):            # 실제 운행 테스트를 하기위한 함수
    print("TakeOff")
    drone.sendTakeOff()
    sleep(0.01)

    print("GoStart")
    drone.sendControlWhile(0,0,0,20,6000)

    drone.sendControlWhile(0,50,-100,5,5000)


    print("GoStop")
    drone.sendControlWhile(0,0,0,0,1000)


    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

def eventAltitude(altitude):
    # print("eventAltitude()")
    # print("- Temperature: {0:.3f}".format(altitude.temperature))
    # print("- Pressure: {0:.3f}".format(altitude.pressure))
    # print("- Altitude: {0:.3f}".format(altitude.altitude))
    print(" 현재 높이 : {0:.3f}".format(altitude.rangeHeight))
    global currentHeight 
    currentHeight = altitude.rangeHeight

def setAltitudeEvent(drone):
    # 이벤트 핸들링 함수 등록
    drone.setEventHandler(DataType.Altitude, eventAltitude)
    # Altitude 정보 요청 
    drone.sendRequest(DeviceType.Drone, DataType.Altitude)
    sleep(0.1)

def readAltitude(drone):
    # Altitude 정보 요청
    drone.sendRequest(DeviceType.Drone, DataType.Altitude)
    sleep(0.1)
    drone.sendRequest(DeviceType.Drone, DataType.Altitude)

def maintainAltitude(drone, goalHeight):
    while True:
        readAltitude(drone)
        print(currentHeight)
        if goalHeight - 0.1 > currentHeight:
            drone.sendControlWhile(0,0,0,20,5)
        elif goalHeight + 0.1 < currentHeight:
            drone.sendControlWhile(0,0,0,-20,5)
        else:
            break

def maintainAltitudeTime(drone, goalHeight, time):
    for i in range(0,int(time/10)):
        readAltitude(drone)
        if goalHeight - 0.1 > currentHeight:
            drone.sendControlWhile(0,0,0,20,10)
        elif goalHeight + 0.1 < currentHeight:
            drone.sendControlWhile(0,0,0,-20,10)
        else:
            drone.sendControlWhile(0,0,0,0,10)

def testAltitude(drone):
    for i in range(0,10):
        # Altitude 정보 요청
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        sleep(1)

    #전진
def straight(roll, pitch, yaw, throttle, time, drone):
    print("Go")
    drone.sendControlWhile(roll, pitch, yaw, throttle, time)

#사각형
def square(drone):
    print("Sqaure")
    print('')
    for i in range(0,4):
        print('각도 전환')
        drone.sendControlWhile(0, 0, -20, 0, 2700)
        sleep(0.1)
        #정지
        drone.sendControlWhile(0,0,0,0,1000)
        sleep(0.1)
        print('사각형 전진')
        # drone.sendControlWhile(0, 30, 0, 0, 2000)
        # sleep(0.1)
        
#8자원
def Circle8(drone):
    drone.sendControlWhile(30,0,-60,0,4500)
    sleep(0.1)
    drone.sendControlWhile(30,0,60,0,4500)
    sleep(0.1)

#zigzag
def zigzag(drone):
    drone.sendControlWhile(0,0,-30,0,500)
    sleep(0.1)
    drone.sendControlWhile( 0, 20,0,0,1500) 
    sleep(0.1)
    drone.sendControlWhile(0,0,60,0,500) 
    sleep(0.1)
    drone.sendControlWhile( 0, 20,0,0,1500) 
    sleep(0.1)
    drone.sendControlWhile(0,0,-60,0,500) 
    sleep(0.1)
    drone.sendControlWhile( 0, 20,0,0,1500)
    sleep(0.1)
    drone.sendControlWhile(0,0,60,0,500) 
    sleep(0.1)
    drone.sendControlWhile( 0, 20,0,0,1500)
    sleep(0.1)
    drone.sendControlWhile(0,0,30,0,500) 
    sleep(0.1)
    



#기능 1 
def GO_1( drone):
    global currentHeight

    #1.호버링 3초
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 3000)
    sleep(0.1)

    # #2. 전진 비행(80cm)
    # straight(0, 20, 0, 0, 2000, drone)
    # sleep(0.1)


    # #3. 고도상승(높이 1.5cm)
    # print("Up")
    # maintainAltitude(drone,1.5)

    # #4. 정지비행(5sec)
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 5000)
    # # maintainAltitudeTime(drone,1.5,100)
    # sleep(0.1)
    
    #4. 사각형 패턴비행(90도 회전, 정지 1sec, 지름 1m 씩)
    square(drone)

    # #5. 정지비행(5sec)
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 5000)
    # sleep(0.1)

    # #6. 원 패턴 비행(지름 1m)    
    # print("Circle")
    # drone.sendControlWhile(30,0,-60,0,4500)

    #7. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    # #8. 후진 비행(1m)
    # print("Back")
    # drone.sendControlWhile(0,-20,0,0,2000)

    # #9. 고도 하강(1m, 50cm 남김)
    # print("Down")
    # maintainAltitude(drone,0.5)

    # #10. 정지 비행(5sec)
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 5000)

def GO_2( drone):
    # #1.호버링 3초
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 3000)

    # #2. 전진 비행(80cm)
    # print("Go")
    # drone.sendControlWhile(0,30,0,0,2000)

    # #3. 고도상승(높이 1.5cm)
    # print("Up")
    # maintainAltitude(drone,1.5)

    #4. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    #5. 8자 원비행(각 원지름 1m)
    print("8Circle")
    Circle8(drone)

    #6. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    #7. 지그재그 비행 4회(45도 방향으로 0.5sec, 전진 1.5sec)
    print("ZigZag")
    zigzag(drone)

    #8. 정지비행(5sec)
    print("Hovering")
    drone.sendControlWhile(0,0,0,0, 5000)

    # #9. 전진 비행(60cm)
    # print("Go")
    # drone.sendControlWhile(0,30,0,0,2000)

    # #10. 고도 하강(높이 50cm)
    # print("Down")
    # maintainAltitude(drone,0.5)

    # #11. 정지 비행(5sec)
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 5000)

    # #12. 고도 상승(높이 1m)
    # print("Up")
    # maintainAltitude(drone,1.0)

    # #13. 전진 비행(50cm)
    # print("Go")
    # drone.sendControlWhile(0,20,0,0,2000)

    # #11. 정지 비행(5sec)
    # print("Hovering")
    # drone.sendControlWhile(0,0,0,0, 5000)
