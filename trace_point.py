import time
import cv2
import numpy as np
import math

image = cv2.VideoCapture(0)
time_previous = 0 #не менять!!!!
frame_rate = 3 #можно менять


while True:
    ret, frame = image.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = 128
    bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
    time_passed = time.time() - time_previous
    if time_passed > (1 / frame_rate): #т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
        time_previous = time.time()
        cv2.imshow('live from your pc :)', bw_frame)

        a = np.array(bw_frame)
        a_size = a.shape
        rows = a_size[0]
        # print(rows)
        columns = a_size[1]
        # print(columns)

        summ_black_ind_x = 0  # индекс среднего черного пикселя в строке
        black_amount_x = 0  # количесвто черных пикселей в строке
        summ_average_row_ind_x = 0  # сумма всех средних индексов по строкам
        black_row_amount_x = 0  # количесвто строк где встречаются черные пиксели

        summ_black_ind_y = 0  # индекс среднего черного пикселя в колонне
        black_amount_y = 0  # количесвто черных пикселей в колонне
        summ_average_row_ind_y = 0  # сумма всех средних индексов по колонне
        black_row_amount_y = 0  # количесвто колонн где встречаются черные пиксели

        sum_rows = np.sum(a, axis = 1)
        sum = 0
        am = 0
        for i in range(rows):
            if (255*rows - sum_rows[i]) != 0:
                sum += i
                am += 1
        crow = sum//am

        sum = 0
        am = 0
        for i in range(coloumns):
            if (255*rows - sum_coloumns[i]) != 0:
                sum += i
                am += 1
        ccol = sum//am

        print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)

    if cv2.waitKey(1) == ord('q'):
         break


bw_frame.release()
cv2.destroyAllWindows()
