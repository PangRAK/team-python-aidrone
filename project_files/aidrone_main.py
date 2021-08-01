from time import sleep
from tkinter.constants import TRUE                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들
import turtle as t
from PIL import ImageTk, Image
import tkinter
import tkinter.font, tkinter.ttk
import threading 




def updateTemp():
    while True:
        global label1, label2
        Height = getHeight()
        cAltitude = getAltitude()
        label1.config(text= '%.2f m'%(Height))
        label2.config(text= '%.2f m'%(cAltitude))
        #print("window !!!!! : "+str(getHeight()) + "      " + str(getAltitude()))
        time.sleep(0.01)


def go1Click(drone):
    t = threading.Thread(target = GO_1, args =(drone,))
    t.start()


def go2Click(drone):
    t = threading.Thread(target = GO_2, args =(drone,))
    t.start()


def go3Click(drone):
    t = threading.Thread(target = GO_3, args =(drone,))
    t.start()


if __name__ == '__main__':
    portName = searchPort()
    for i in range(3,0,-1):
        print(i)
        sleep(1)

    drone = Drone()
    drone.open("COM7")    # 컨트롤러와 연결된 포트 번호
    setTrim(drone)          # 시작 전 Trim 초기화
    setEvent(drone)         # EventHandler 세팅 (Altitude와 Attitude)



    

    #GUI
    window = tkinter.Tk()
    window.geometry("900x650")
    window.resizable(TRUE, TRUE)

    #미션 1,2,3
    btn1 = tkinter.Button(window, text = 'Go 1', width = 20, height= 2, relief = 'solid', command=lambda : go1Click(drone))
    btn2 = tkinter.Button(window, text = 'Go 2', width = 20, height= 2, relief = 'solid', command=lambda : go2Click(drone))
    btn3 = tkinter.Button(window, text = "Go 3", relief = 'solid', width = 20, height= 2, command=lambda : go3Click(drone))
    btn1.place(x = 30, y =20)
    btn2.place(x = 370, y = 20)
    btn3.place(x = 720, y = 20)

    ##캔버스 배치를 위한 프레임##
    cframe=tkinter.Frame(window, background="white",width = 850, height= 450)
    canvas = tkinter.Canvas(master = cframe,width = 850, height= 450)
    p = t.TurtleScreen(canvas)
    cframe.place(x = 20, y = 100)
    canvas.pack()
    #거북이 객체
    tt = t.RawTurtle(p)
    # img = ImageTk.PhotoImage(Image.open('drone_img.png'))
    # t.register_shape("Pic",Shape("image",img))
    # tt.shape("Pic")



    

    #글씨체
    font1 = tkinter.font.Font(family="맑은 고딕", size=20 , weight = "bold")
    font2 = tkinter.font.Font(family="맑은 고딕", size=11 , weight = "bold")

    # 높이
    label3 = tkinter.Label(window,  text = "        현재 높이 :    ", font = font1)
    label4 = tkinter.Label(window, text = "        고도  :   ", font = font2)
    label1 = tkinter.Label(window,text = '0.0', font = font1)
    label2 = tkinter.Label(window,text = '0.0', font = font2)
    label3.place(x=530,y=560)
    label1.place(x=770,y=560)
    label4.place(x=700,y=610)
    label2.place(x=800,y=610)

    threading.Thread(target=updateTemp, daemon=True).start()

    window.mainloop()
    #GO_3(drone)



    drone.close()
