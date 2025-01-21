import time
import cv2
import numpy as np
import math
from itertools import count


def get_black_line(frame, nearby_pixels, edge):
    if frame is None:
        return

    height = frame.shape[0]
    width = frame.shape[1]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # TODO сделать регулировку парараметров у blure и adaptiveThreshold
    blurred_frame = cv2.GaussianBlur(gray_frame, (19, 19), 0)
    bw_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nearby_pixels, edge)

    # верхняя часть массива
    sum_columns_top = np.sum(bw_frame[0 : height // 2], axis=0)

    sum_left = 0
    sum_right = 0
    i_left = 0
    i_right = width - 1

    while i_left != i_right:
        if (sum_left < sum_right):
            sum_left += 255 * height // 2 - sum_columns_top[i_left]
            i_left += 1
        else:
            sum_right += 255 * height // 2 - sum_columns_top[i_right]
            i_right -= 1

    target_circle_x = i_left
    target_circle_y = height // 4

    cv2.circle(bw_frame, (target_circle_x, target_circle_y), 10, 155, thickness=20)

    # средняя часть массива
    sum_columns_center = np.sum(bw_frame[height // 4 : 3 * height // 4], axis=0)

    sum_left = 0
    sum_right = 0
    i_left = 0
    i_right = width - 1

    while i_left != i_right:
        if (sum_left < sum_right):
            sum_left += 255 * height // 2 - sum_columns_center[i_left]
            i_left += 1
        else:
            sum_right += 255 * height // 2 - sum_columns_center[i_right]
            i_right -= 1

    start_circle_x = i_left
    start_circle_y = height // 2
    cv2.circle(bw_frame, (start_circle_x, start_circle_y), 10, 155, thickness=20)

    color_for_arrow = (0, 0, 255)
    bw_frame = cv2.arrowedLine(bw_frame, (start_circle_x, start_circle_y), (target_circle_x, target_circle_y), color_for_arrow, 2)

    return (target_circle_x, bw_frame, target_circle_x - width // 2, math.atan2(target_circle_x - start_circle_x, height//4))
