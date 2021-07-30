from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들
import turtle as t
import test

if __name__ == '__main__':
    portName = searchPort()
    for i in range(3,0,-1):
        print(i)
        sleep(1)

    drone = Drone()
    drone.open(portName)    # 컨트롤러와 연결된 포트 번호
    setTrim(drone)          # 시작 전 Trim 초기화
    setEvent(drone)         # EventHandler 세팅 (Altitude와 Attitude)
    print("TakeOff") 
    takeOff(drone)          # 이륙
    drone.sendControlWhile(0,0,0,0,3000)
    sleep(0.1)

    # 여기 실행코드 
    # 미션1 : Go_1
    # 미션2 : Go_2
    # 미션3 : Go_3
    GO_3(drone)

    #테스트용
    # while True:
    #     drone.sendRequest(DeviceType.Drone, DataType.Attitude)
    #     sleep(1)

    print("Landing")
    landing(drone)      # 착륙

    drone.close()
