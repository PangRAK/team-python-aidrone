from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from pynput import keyboard                  # 드론 라이브러리
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들
from turtle import *

if __name__ == '__main__':
    searchPort()
    for i in range(5,0,-1):
        print(i)
        sleep(1)

    drone = Drone()
    drone.open('COM7')  # 컨트롤러와 연결된 포트 번호

    print("start")
    testMove(drone)
    print("stop")

    drone.close()