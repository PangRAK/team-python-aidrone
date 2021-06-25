from time import sleep
from e_drone.drone import *
from e_drone.protocol import *

def eventButton(button):
    print(button.button)

def eventJoystick(joystick):
    print(joystick.left.x, joystick.left.y, joystick.right.x, joystick.right.y)

if __name__ == '__main__':
    drone = Drone()
    drone.open('COM7')
    drone.setEventHandler(DataType.Button, eventButton)
    drone.sendPing(DeviceType.Controller)
    drone.setEventHandler(DataType.Joystick, eventJoystick)
    drone.sendPing(DeviceType.Controller)
    for i in range(10,0,-1):
        print(i)
        sleep(1)

    drone.close()