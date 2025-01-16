import time
from itertools import count

import cv2
import numpy as np
import math
from pioneer_sdk import Camera


def get_black_point(frame):
    if frame is None:
        return

    a_size = frame.shape

    rows = a_size[0]
    columns = a_size[1]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (19, 19), 0)
    bw_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 15)
    a = np.array(bw_frame)

    sum_rows = np.sum(a, axis=1)
    sum_columns = np.sum(a, axis=0)
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
                if (255 * columns - sum_rows[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 1", i)
            while sum2 < sum1:
                if (255 * columns - sum_rows[rows - j - 1]) != 0:
                    sum2 += 1
                    right = rows - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в первом")
    ccol = (right + left) // 2

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
                if (255 * rows - sum_columns[i]) != 0:
                    sum1 += 1
                    left = i
                i += 1
                # print("i in while 2", i)
            while sum2 <= sum1:
                if (255 * rows - sum_columns[columns - j - 1]) != 0:
                    sum2 += 1
                    right = columns - 1 - j
                j += 1
    except IndexError:
        pass
        # print("выход за границе в втором")
    # print(right, left)
    crow = (right + left) // 2

    bw_frame = cv2.circle(bw_frame, (crow, ccol), 10, 155, thickness=20)
    # print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

    # print("imshow")


    return (crow, ccol, bw_frame)


if __name__ == "__main__":
    camera = Camera()

    while True:
        get_black_point(camera.get_cv_frame())
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
