import time
import cv2
import numpy as np
import math
from pioneer_sdk import Camera


# image = cv2.VideoCapture(0)
camera = Camera()
time_previous = 0  # не менять!!!!
frame_rate = 1000  # можно менять

thresh = 100

while True:
    frame = camera.get_cv_frame()
    if frame is None:
        continue

    a_size = frame.shape

    rows = a_size[0]
    columns = a_size[1]

    time_passed = time.time() - time_previous
    if time_passed > (1 / frame_rate): #т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
        time_previous = time.time()
        a = np.array(bw_frame)

        sum_rows = np.sum(a, axis = 1)
        sum_columns = np.sum(a, axis = 0)
        sum1 = 0
        sum2 = 0
        i = 0
        j = 0
        left = 0
        right = rows - 1
        while i<(rows-1-j):
            while sum1 <= sum2:
                if (255*columns - sum_rows[i]) != 0:
                    sum1 += 1
                    left = i
                i +=1
            while sum2 < sum1:
                if (255*columns - sum_rows[rows-j-1]) != 0:
                    sum2 += 1
                    right = rows-1 - j
                j+=1 
        ccol = (right+left)//2


        sum1 = 0
        sum2 = 0
        i = 0
        j = 0
        left = 0
        right = columns - 1
        print(right, left)
        while i < (columns-1-j):
            while sum1 <= sum2:
                if (255*rows - sum_columns[i]) != 0:
                    sum1 += 1
                    left = i
                i +=1
            while sum2 <= sum1:
                if (255*rows - sum_columns[columns-j-1]) != 0:
                    sum2 += 1
                    right = columns-1 - j
                j+=1 
        print(right, left)
        crow = (right+left)//2
        
        bw_frame = cv2.circle(bw_frame, (crow, ccol), 10, 155, thickness=20)
        # print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

      
    cv2.imshow('live from your pc :)', bw_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('m'):
        thresh -= 10
    if key == ord('p'):
        thresh += 10


bw_frame.release()
cv2.destroyAllWindows()
