import time
import cv2
import numpy as np
import math

image = cv2.VideoCapture(0)
time_previous = 0 #не менять!!!!
frame_rate = 1 #можно менять

thresh = 100
ret, frame = image.read()
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
a = np.array(bw_frame)
a_size = a.shape

rows = a_size[0]
columns = a_size[1]
while True:
    thresh = 100
    ret, frame = image.read()
    time_passed = time.time() - time_previous
    if time_passed > (1 / frame_rate): #т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
        time_previous = time.time()
        a = np.array(bw_frame)

        sum_rows = np.sum(a, axis = 1)
        sum = 0
        am = 0
        for i in range(rows):
            if (255*columns - sum_rows[i]) != 0:
                sum += i
                am += 1
        if am != 0:
            crow = sum//am
        else:
            crow = 0
            print("Bah")

        sum_columns = np.sum(a, axis = 0)
        sum = 0
        am = 0
        for i in range(columns):
            if (255*rows - sum_columns[i]) != 0:
                sum += i
                am += 1
        if am != 0:
            ccol = sum//am
        else:
            ccol = 0
            print("Bah")
        bw_frame[crow][ccol] = 255  
        print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

      
    cv2.imshow('live from your pc :)', bw_frame)
    if cv2.waitKey(1) == ord('q'):
         break


bw_frame.release()
cv2.destroyAllWindows()
