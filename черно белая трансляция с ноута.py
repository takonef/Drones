import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = 128
    bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('live from your pc :)', bw_frame)

    if cv2.waitKey(1) == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()

