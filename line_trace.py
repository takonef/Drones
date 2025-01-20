import time
from itertools import count

import cv2
import numpy as np
import math
from pioneer_sdk import Camera


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
    a_top = a[:len(a)//2] #верхняя часть массива
    a_bottom = a[len(a)//2:] #нижняя часть массива

    sum_rows_top = np.sum(a_top, axis=1)
    sum_columns_top = np.sum(a_top, axis=0)
    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = rows - 1
    # print("columns", columns)
    # print("rows", rows)
    try:
        while i < (rows - 1 - j):
            while sum1 <= sum2:
                if (255 * columns - sum_rows_top[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 1", i)
            while sum2 < sum1:
                if (255 * columns - sum_rows_top[rows - j - 1]) != 0:
                    sum2 += 1
                    right = rows - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в первом")
    ccol_top = (right + left) // 2

    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = columns - 1
    # print(right, left)
    try:
        while i < (columns - 1 - j):
            while sum1 <= sum2:
                if (255 * rows - sum_columns_top[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 2", i)
            while sum2 <= sum1:
                if (255 * rows - sum_columns_top[columns - j - 1]) != 0:
                    sum2 += 1
                    right = columns - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в втором")
    # print(right, left)
    crow_top= (right + left) // 2

    frame = cv2.circle(bw_frame, (crow_top, ccol_top), 10, 155, thickness=20)
    # print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

    # print("imshow")


    ###return (crow_top, ccol_top, bw_frame)

    sum_rows_bottom = np.sum(a_bottom, axis=1)
    sum_columns_bottom = np.sum(a_bottom, axis=0)
    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = rows - 1
    # print("columns", columns)
    # print("rows", rows)
    try:
        while i < (rows - 1 - j):
            while sum1 <= sum2:
                if (255 * columns - sum_rows_bottom[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 1", i)
            while sum2 < sum1:
                if (255 * columns - sum_rows_bottom[rows - j - 1]) != 0:
                    sum2 += 1
                    right = rows - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в первом")
    ccol_bottom = (right + left) // 2

    sum1 = 0
    sum2 = 0
    i = 0
    j = 0
    left = 0
    right = columns - 1
    # print(right, left)
    try:
        while i < (columns - 1 - j):
            while sum1 <= sum2:
                if (255 * rows - sum_columns_bottom[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 2", i)
            while sum2 <= sum1:
                if (255 * rows - sum_columns_bottom[columns - j - 1]) != 0:
                    sum2 += 1
                    right = columns - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в втором")
    # print(right, left)
    crow_bottom = (right + left) // 2

    bw_frame = cv2.circle(bw_frame, (crow_bottom, ccol_bottom), 10, 155, thickness=20)
    # print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

    # print("imshow")


    ###return (crow_bottom, ccol_bottom, bw_frame)
    color_for_arrow = (0, 0, 255)
    bw_frame = cv2.arrowedLine(bw_frame, (ccol_bottom, crow_bottom), (ccol_top, crow_top), color_for_arrow, 2)
    return ('crow_top, ccol_bottom, crow_bottom, ccol_bottom', crow_top, ccol_bottom, crow_bottom, ccol_bottom, bw_frame)


if __name__ == "__main__":
    camera = Camera()

    while True:
        get_black_point(camera.get_cv_frame())
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
