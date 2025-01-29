import cv2
import numpy as np

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #перевод bgr изображения в серое, теперь оно двухмерное, каждый пискель имеет значение от 0(черный) до 255(белый)
    thresh = 128 #устанавливаем границу
    bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1] #threshold: все что меньше установленной границы - черное, больше - белое
    cv2.imshow('live from your pc :)', bw_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
