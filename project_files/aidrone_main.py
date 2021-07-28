from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from pynput import keyboard                  # 드론 라이브러리
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들
import turtle as t
import test

if __name__ == '__main__':
    searchPort()
    for i in range(5,0,-1):
        print(i)
        sleep(1)

    # mturtle = t.Turtle()
    drone = Drone()
    drone.open('COM7')  # 컨트롤러와 연결된 포트 번호
    # test.droneGui(drone)
    setTrim(drone)
    setAltitudeEvent(drone)
    print("start")
    takeOff(drone)      # 이륙

    # 여기 실행코드
    GO_1(drone)

    landing(drone)      # 착륙
    print("stop")

    drone.close()
