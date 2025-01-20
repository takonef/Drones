import cv2
import numpy as np
import time
from pioneer_sdk import Pioneer
from camera_pio import *
import threading

global_frame = None

def camera_start():
    global global_frame
    while True:
        global_frame = get_cv_frame()

th1 = threading.Thread(target=camera_start)
th1.start()

thresh = 100

while True:
    frame = global_frame
    print(global_frame)
    if frame is not None:
        print('frames')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
        frame = np.vectorize(lambda x: 255-x)(bw_frame).astype(np.uint8)

        rows = frame.shape[0]
        columns = frame.shape[1]

 # коэффицент края (на квадратики вокруг центра)
        for i in range(rows):
            for j in range(columns):
                if (i < rows/8) or (i > 7*rows/8) or (j < columns/8) or (j > 7*columns/8):
                    frame[i][j] = frame[i][j]//10
                elif (i < rows/4) or (i > 3*rows/4) or (j < columns/4) or (j > 3*columns/4):
                    frame[i][j] = frame[i][j]//4

        columns_sum = np.sum(frame, axis=0)
        left_index = 0
        right_index = rows - 1
        left_sum = 0
        right_sum = 0
        while left_index != right_index:
            if (left_sum < right_sum):
                left_sum += columns_sum[left_index]
                left_index += 1
            else:
                right_sum += columns_sum[right_index]
                right_index -= 1

        rows_sum = np.sum(frame, axis=1)
        top_index = 0
        bottom_index = rows - 1
        top_sum = 0
        bottom_sum = 0
        while top_index != bottom_index:
            if (top_sum < bottom_sum):
                top_sum += rows_sum[top_index]
                top_index += 1
            else:
                bottom_sum += rows_sum[bottom_index]
                bottom_index -= 1

        frame = cv2.circle(frame, (left_index, top_index), 2, 100, thickness=2)
        cv2.imshow('live from your pc :)', frame)

    if cv2.waitKey(1) == ord('q'):
         break

cv2.destroyAllWindows()
