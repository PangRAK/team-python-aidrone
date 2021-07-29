from time import sleep                          # 슬립 라이브러리
from e_drone.drone import *                     # 드론 라이브러리
from e_drone.protocol import *
from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
from aidrone_function import *                  # 내가 지정한 함수들
import turtle as t

import cv2
import numpy as np

if __name__ == '__main__':
    searchPort()    
    cap = cv2.VideoCapture(0)
    eye_detector = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

    for i in range(3,0,-1):
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
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_detector.detectMultiScale(gray, 1.3, 5)
        # print(eyes[0,0])
        if type(eyes) != tuple:
            x, y, w, h = eyes[0]
            roi = frame[y: (y+h), x: (x+w)]
            rows, cols, _ = roi.shape
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (31,31), 0)
            
            _, threshold = cv2.threshold(gray_roi, 40, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            
            for cnt in contours:
                (x2,y2,w2,h2) = cv2.boundingRect(cnt)
                cv2.rectangle(roi, (0,0), (w, h), (0, 255, 0), 2)
                cv2.line(roi, (x2+int(w2/2), 0), (x2+int(w2/2), rows), (0, 255, 0), 2)
                cv2.line(roi, (0, y2+int(h2/2)), (cols, y2+int(h2/2)), (0, 255, 0), 2)
                cv2.drawContours(roi, [cnt], -1, (0,0,255),2)
                x_rate = (x2+int(w2/2)) / rows
                y_rate = (y2+int(h2/2)) / cols
                print(x_rate, '  ', y_rate)
                # if(x_rate < 0.40):
                #     print('왼쪽')
                #     drone.sendControlWhile(0,0,10,0,2000)
                # elif(x_rate > 0.65):
                #     print('오른쪽')
                #     drone.sendControlWhile(0,0,-10,0,2000)
                # elif(y_rate > 0.52):
                #     print('아래')
                #     drone.sendControlWhile(0,10,0,0,2000)
                # elif(y_rate < 0.42):
                #     print('위')
                #     drone.sendControlWhile(0,-10,0,0,2000)
                # break
            
            cv2.imshow("gray roi", gray_roi)
            cv2.imshow("Threshold", threshold)
            cv2.imshow("Roi", roi)
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(30)
            if key == 27:
                break

    cv2.destroyAllWindows()





    landing(drone)      # 착륙
    print("stop")

    drone.close()


# from time import sleep                          # 슬립 라이브러리
# from e_drone.drone import *                     # 드론 라이브러리
# from e_drone.protocol import *
# from pynput import keyboard                  # 드론 라이브러리
# from serial.tools.list_ports import comports    # 포트 번호 가져올 수 있는 라이브러리
# from aidrone_function import *                  # 내가 지정한 함수들
# import turtle as t

# import cv2
# import numpy as np

# if __name__ == '__main__':
#     searchPort()    
#     cap = cv2.VideoCapture(0)
#     # eye_detector = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

#     for i in range(3,0,-1):
#         print(i)
#         sleep(1)

#     # mturtle = t.Turtle()
#     drone = Drone()
#     drone.open('COM7')  # 컨트롤러와 연결된 포트 번호
#     # test.droneGui(drone)
#     setTrim(drone)
#     setAltitudeEvent(drone)
#     print("start")
#     takeOff(drone)      # 이륙

#     # 여기 실행코드
#     while True:
#         ret, frame = cap.read()
#         frame = cv2.flip(frame,1)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (7,7), 0)
#         rows, cols = gray.shape
        
#         # eyes = eye_detector.detectMultiScale(gray, 1.3, 5)
#         # print(eyes[0,0])
#         # if type(eyes) != tuple:
#             # x, y, w, h = eyes[0]
#             # roi = frame[y: (y+h), x: (x+w)]
#             # rows, cols, _ = roi.shape
#             # gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#             # gray_roi = cv2.GaussianBlur(gray_roi, (7,7), 0)
        
#         _, threshold = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY_INV)
#         contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        
#         for cnt in contours:
#             (x2,y2,w2,h2) = cv2.boundingRect(cnt)
#             # cv2.rectangle(roi, (0,0), (w, h), (0, 255, 0), 2)
#             cv2.line(frame, (x2+int(w2/2), 0), (x2+int(w2/2), rows), (0, 255, 0), 2)
#             cv2.line(frame, (0, y2+int(h2/2)), (cols, y2+int(h2/2)), (0, 255, 0), 2)
#             cv2.drawContours(frame, [cnt], -1, (0,0,255),2)
#             x_rate = (x2+int(w2/2)) / rows
#             y_rate = (y2+int(h2/2)) / cols
#             print(x_rate, '  ', y_rate)
#             if(x_rate < 0.43):
#                 print('왼쪽')
#                 drone.sendControlPosition(0,0,0,0,-10,10)
#             elif(x_rate > 0.6):
#                 print('오른쪽')
#                 drone.sendControlPosition(0,0,0,0,10,10)
#             elif(y_rate > 0.55):
#                 print('아래')
#                 drone.sendControlPosition(0.1,0,0,0.1,0,0)
#             elif(y_rate < 0.45):
#                 print('위')
#                 drone.sendControlPosition(-0.1,0,0,0.1,0,0)
#             break
            
#         # cv2.imshow("gray roi", gray_roi)
#         cv2.imshow("Threshold", threshold)
#         # cv2.imshow("Roi", roi)
#         cv2.imshow("Frame", frame)

#         key = cv2.waitKey(30)
#         if key == 27:
#             break

#     cv2.destroyAllWindows()

#     landing(drone)      # 착륙
#     print("stop")

#     drone.close()