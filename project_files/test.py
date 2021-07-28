from turtle import *
from tkinter import *
from time import *
import tkinter.font, tkinter.ttk
from aidrone_function import *
from e_drone import *


class droneGui(object):
    def __init__(self,drone):

        self.window = Tk()

        self.window.geometry("640x400+100+100")
        self.window.resizable(False, False)
        
        var1= StringVar()
        var2= StringVar()
        var1.set('0.0')
        var2.set('0.0')
        #입력 부분 배치를 위한 프레임 선언##
        frame=Frame(self.window)

        font1 = tkinter.font.Font(family="맑은 고딕", size=12 , weight = "bold")
        font2 = tkinter.font.Font(family="맑은 고딕", size=9 , weight = "bold")
  
        label3 = Label(self.window, text = "        현재 높이 :     ", font = font1)
        label4 = Label(self.window, text = "        고도 :     ",  font = font2)
        label3.pack(side= "left")
        label4.pack(side="left")
        label1 = Label(self.window, textvariable = var1, font = font1)
        label2 = Label(self.window, textvariable = var2,  font = font2)
        label1.pack(side='left')
        label2.pack(side='left')

        # cframe = Frame(self.window, background="white")
        # canvas = Canvas(master = cframe)
        # t = RawTurtle(canvas)

        # cframe.pack(side="left", fill="both", expand=True)
        # canvas.pack(side="left", fill="both", expand=True)

        #터틀 모양 t.shape("")
        readAltitude(drone)
        var1.set(recvHeight())
        var2.set(recvAltitude())

        self.window.mainloop()