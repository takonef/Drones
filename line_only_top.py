import time
import cv2
import numpy as np
import math
from itertools import count


def get_black_line(frame):
    if frame is None:
        return

    a_size = frame.shape

    rows = a_size[0]
    columns = a_size[1]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #TODO сделать регулировку парараметров у blure и adaptiveThreshold
    blurred_frame = cv2.GaussianBlur(gray_frame, (19, 19), 0)
    bw_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 15)
    a = np.array(bw_frame)

    #верхняя часть массива
    sum_rows_top = np.sum(a[:len(a)//2], axis=1)
    sum_columns_top = np.sum(a[:len(a)//2], axis=0)

    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = rows - 1
    try:
        while i < (rows//2 - 1 - j):
            while sum1 <= sum2:
                if (255 * columns - sum_rows_top[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
            while sum2 < sum1:
                if (255 * columns - sum_rows_top[rows//2 - j - 1]) != 0:
                    sum2 += 1
                    right = rows//2 - 1 - j
                j += 1
    except IndexError:
        # print("выход за границе в первом")
        pass

    ccol_top = (right + left) // 2

    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = columns - 1

    try:
        while i < (columns - 1 - j):
            while sum1 <= sum2:
                if (255 * rows//2 - sum_columns_top[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
            while sum2 <= sum1:
                if (255 * rows//2 - sum_columns_top[columns - j - 1]) != 0:
                    sum2 += 1
                    right = columns - 1 - j
                j += 1
    except IndexError:
        # print("выход за границе в втором")
        pass

    crow_top = (right + left) // 2
    cv2.circle(bw_frame, (crow_top, ccol_top), 10, 155, thickness=20)

    crow_bottom = columns // 2
    ccol_bottom = rows // 2
    cv2.circle(bw_frame, (crow_bottom, ccol_bottom), 10, 155, thickness=20)

    # print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)
    color_for_arrow = (0, 0, 255)
    bw_frame = cv2.arrowedLine(bw_frame, (crow_bottom, ccol_bottom), (crow_top, ccol_top), color_for_arrow, 2)
    
    return (bw_frame, crow_bottom-crow_top)

# image = cv2.VideoCapture(0)
# time_previous = 0 #не менять!!!!
# frame_rate = 24 #можно менять

# thresh = 100
# ret, frame = image.read()
# gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
# bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
# a = bw_frame
# a_size = a.shape

# rows = a_size[0]
# columns = a_size[1]
# print(rows, columns)

# while True:
#     ret, frame = image.read()
#     time_passed = time.time() - time_previous
#     if time_passed > (1 / frame_rate): #т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
#         bw_frame, delta = get_black_line(frame)
#         print(delta)
      
#     cv2.imshow('live from your pc :)', bw_frame)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

# image.release()
# cv2.destroyAllWindows()

# if __name__ == "__main__":
#     camera = Camera()

#     while True:
#         get_black_point(camera.get_cv_frame())
#         key = cv2.waitKey(1)
#         if key == ord('q'):
#             break

#     cv2.destroyAllWindows()
