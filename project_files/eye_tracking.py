import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# c                                                                                                                                                                                    ap.set(3, 640) # set video width
# cap.set(4, 480) # set video height
eye_detector = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_detector.detectMultiScale(gray, 1.3, 5)
    # print(eyes[0,0])
    if type(eyes) != tuple:
        x, y, w, h = eyes[0]
        roi = frame[y: (y+h), x: (x+w)]
        rows, cols, _ = roi.shape
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # gray_roi = cv2.GaussianBlur(gray_roi, (7,7), 0)
        
        _, threshold = cv2.threshold(gray_roi, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        
        for cnt in contours:
            (x2,y2,w2,h2) = cv2.boundingRect(cnt)
            cv2.rectangle(roi, (0,0), (w, h), (0, 255, 0), 2)
            cv2.line(roi, (x2+int(w2/2), 0), (x2+int(w2/2), rows), (0, 255, 0), 2)
            cv2.line(roi, (0, y2+int(h2/2)), (cols, y2+int(h2/2)), (0, 255, 0), 2)
            cv2.drawContours(roi, [cnt], -1, (0,0,255),2)
            print((x2+int(w2/2)) / rows, '  ', (y2+int(h2/2)) / cols)
            break

        # cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)     
        # for (x,y,w,h) in eyes:
        #     # Save the captured image into the datasets folder
        #     cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        #     cv2.imshow('image', img)
        
        # cv2.imshow("Frame", frame)
        # cv2.imshow("Roi", roi)
        cv2.imshow("gray roi", gray_roi)
        cv2.imshow("Threshold", threshold)
        cv2.imshow("Roi", roi)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(30)
        if key == 27:
            break

cv2.destroyAllWindows()