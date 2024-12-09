import numpy as np
import cv2
import math


image_gray = cv2.imread("/Users/annkarodionova/Desktop/lol.png", cv2.IMREAD_GRAYSCALE) #картинку любую вставляй
thresh = 128 #пограничное значение, ниже него - белое, больше - черное
image_bw = cv2.threshold(image_gray, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("image", image_bw)
a = np.array(image_bw)

summ_black_ind_x = 0 #индекс среднего черного пикселя в строке
black_amount_x = 0 #количесвто черных пикселей в строке
summ_average_row_ind_x = 0 #сумма всех средних индексов по строкам
black_row_amount_x = 0 #количесвто строк где встречаются черные пиксели

summ_black_ind_y = 0 #индекс среднего черного пикселя в колонне
black_amount_y = 0 #количесвто черных пикселей в колонне
summ_average_row_ind_y = 0 #сумма всех средних индексов по колонне
black_row_amount_y = 0 #количесвто колонн где встречаются черные пиксели


a_size = a.shape
rows = a_size[0]
#print(rows)
columns = a_size[1]
#print(columns)

#ищем среднее значение в строках, те х, но на самом деле выходит номер колонны
for i in range(rows):
    for j in range(columns):
        if a[i][j] == 0:
            #print('row:', i, 'column:', j)
            summ_black_ind_x += j #считаем для i строки сумму индексов черных пикселей
            black_amount_x += 1 #считаем для i строки количество черных пискелей
    if summ_black_ind_x != 0:
        summ_average_row_ind_x += math.ceil(summ_black_ind_x / black_amount_x) #сумма всех средних индексов
    if black_amount_x != 0:
        black_row_amount_x += 1
        average_black_ind_x = math.ceil(summ_average_row_ind_x / black_row_amount_x) #финальный средний индекс по иксу
    summ_black_ind_x = 0 #обнуляем значение для следующей строки
    black_amount_x = 0 #обнуляем значение для следующей строки



#ищем среднее значение в колоннах, по факту это высота, те игрек, на самом деле выходит номер ряда
for k in range(columns):
    for h in range(rows):
        if a[h][k] == 255:
            #print('row:', h, 'column:', k)
            summ_black_ind_y += h #считаем для k колонны сумму индексов черных пикселей
            black_amount_y += 1 #считаем для k колонны количество черных пискелей
    if summ_black_ind_y != 0:
        summ_average_row_ind_y += math.ceil(summ_black_ind_y / black_amount_y) #сумма всех средних индексов

    if black_amount_y != 0:
        black_row_amount_y += 1
        average_black_ind_y = math.ceil(summ_average_row_ind_y / black_row_amount_y) #финальный средний индекс по игреку
    summ_black_ind_y = 0 #обнуляем значение для следующей колонны
    black_amount_y = 0 #обнуляем значение для следующей колонны


print(average_black_ind_y, average_black_ind_x) #ряд(высота - у) и колонна(сторона - х)



cv2.waitKey(0) == ord('q')
cv2.destroyAllWindows()

