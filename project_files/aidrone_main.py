from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *                  # 드론 라이브러리
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from turtle import *

def searchPort():                # 포트 검색 함수    
    # for port, desc, hwid in sorted(comports()):
    #     print('%s' % (port))
        
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

def joystickGoto(joystick):    # 조이스틱 입력 정보 함수
    goto(joystick.right.x, joystick.right.y)

def eventMotion(motion):
    print("eventMotion()")
    print("Accel    :   {0:5},  {1:5},  {2:5}",format(motion.accelX,motion.accelY,motion.accelZ))
    print("Gyro     :   {0:5},  {1:5},  {2:5}",format(motion.gyroRoll,motion.gyroPitch,motion.gyroYaw))
    print("Angle    :   {0:5},  {1:5},  {2:5}",format(motion.angleRoll,motion.anglePitch,motion.angleYaw))

def randomLight():
    for i in range(0,10,1):
        r = int(random.randint(0, 255))
        g = int(random.randint(0, 255))
        b = int(random.randint(0, 255))

        dataArray = drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, r, g, b)

        sleep(2)

def testHovering():
    print("TakeOff")
    drone.sendTakeOff()
    sleep(0.01)

    print("Hovering")
    drone.sendControlWhile(0,0,0,0,7000)

    print("Go Stop")
    drone.sendControlWhile(0,0,0,0,1000)

    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

def readEvent():
    drone.setEventHandler(DataType.Button, eventButton)     # 버튼 이벤트와 연결할 함수를 지정
    drone.setEventHandler(DataType.Joystick, joystickGoto) # 조이스틱 이벤트와 연결할 함수를 지정
    drone.setEventHandler(DataType.Motion, eventMotion)
    drone.sendPing(DeviceType.Controller)

    while True:
        drone.sendRequest(DeviceType.Drone,DataType.Motion)
        sleep(1)
        if KeyboardInterrupt:
            break;

def eventTrim(trim):
    print("{0}, {1}, {2}, {3}".format(trim.roll,trim.pitch,trim.yaw,trim.throttle))

def setTrim():
    drone.setEventHandler(DataType.Trim,eventTrim)

    drone.sendTrim(0,0,0,0)
    sleep(0.01)

    drone.sendRequest(DeviceType.Drone,DataType.Trim)
    sleep(0.01)

def testMove():
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

if __name__ == '__main__':
    searchPort()
    for i in range(5,0,-1):
        print(i)
        sleep(1)

    drone = Drone()
    drone.open('COM7')                                      # 컨트롤러와 연결된 포트 번호

    setTrim()
    testMove()
    
    drone.close()