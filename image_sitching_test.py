import cv2
from pioneer_sdk import Camera


imgs = []

camera = Camera()

while True:
    frame = camera.get_cv_frame()
    if frame is not None:
        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)
        if key == 27:  # esc
            print("esc pressed")
            cv2.destroyAllWindows()
            break
        elif key == ord("1"):
            imgs.append(frame)
            print(imgs)


stitcher = cv2.Stitcher.create(cv2.STITCHER_SCANS)
status, full_map = stitcher.stitch(imgs)

if status != cv2.Stitcher_OK:
        print("Невозможно склеить изображения, код ошибки = %d" % status)

cv2.imshow('stitched image', full_map)
cv2.waitKey(0)
cv2.destroyAllWindows()

