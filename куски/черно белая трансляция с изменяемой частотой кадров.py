import time
import cv2
import numpy as np

image = cv2.VideoCapture(0)
time_previous = 0 #не менять!!!!
frame_rate = 5 #можно менять

while True:
    ret, frame = image.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = 128
    bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
    time_passed = time.time() - time_previous
    if time_passed > (1 / frame_rate): #т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
        time_previous = time.time()
        cv2.imshow('live from your pc :)', bw_frame)

    if cv2.waitKey(1) == ord('q'):
         break


bw_image.release()
cv2.destroyAllWindows()
