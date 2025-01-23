import cv2
import numpy as np
import time
from pioneer_sdk import Pioneer
from camera_pio import *
import threading
import socket
from line_only_top import *
import traceback
from aruco_detect import *

global_frame = None

def camera_start():
    global global_frame
    while True:
        global_frame = get_cv_frame()

th1 = threading.Thread(target=camera_start)
th1.start()

# def detect_aruco(detector):


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

nearby_pixels = 61
edge = 15
if __name__ == "__main__":
    print(
        """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land

    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓"""
    )
    is_control_by_PID = False
    centered = False
    pioneer_mini = Pioneer()
    # camera = Camera()
    min_v = 1300
    max_v = 1700
    try:
        while True:
            frame = global_frame
            print(global_frame)
                if frame is not None:    
                ch_1 = 1500
                ch_2 = 1500
                ch_3 = 1500
                ch_4 = 1500
                ch_5 = 2000
                frame = camera.get_cv_frame()
    
    
    
                if frame is None:
                    continue
    
                yc, xc, _ = frame.shape
                yc //= 2
                xc //= 2
                yc -= 1
                xc -= 1
    
                target_circle_x, frame_after_thresh, dx_center, dangle = get_black_line(frame, nearby_pixels, edge)
    
    
    
                    # print("dVx, dVy", dVx, dVy)
                dVx_aruco, dVy_aruco, dx, dy = aruco_detected(detector, frame, xc, yc)
                if dVx_aruco > 0 and dVy_aruco > 0:
                    color_for_arrow = (255, 0, 0)
                    frame = cv2.arrowedLine(frame, (xc, yc), (xc + dx, yc + dy), color_for_arrow, 2)
                    ch_3 = 1500 + int(dVy_aruco)
                    ch_4 = 1500 + int(dVx_aruco)
                    ch_1 = 1400 #вниз
    
                dV_max = 300
                dVx = dV_max * (dx_center / xc)
                # print(dangle)
    
                dVrot_k = 250
    
                limit = 170
                if dVx > limit:
                    dVx = limit
                if dVx < -limit:
                    dVx = -limit
    
                if not is_control_by_PID:
                    dx = 0
                    color = [0, 0, 255]
                else:
                    if target_circle_x == 0:
                        is_control_by_PID = not is_control_by_PID
                        print("you have reached the destination")
                        # time.sleep(2)
                        # pioneer_mini.land()
    
                    ch_2 = 1500 - int(dVrot_k * dangle)
                    ch_4 = 1500 + int(dVx)
                    ch_3 = 1430  # 1350
                    # ch_3 = 1500
                    color = [0, 255, 0]
                    frame = cv2.circle(frame, (10, 10), 10, color, cv2.FILLED)
    
                key = cv2.waitKey(1)
                if key == 27:  # esc
                    print("esc pressed")
                    cv2.destroyAllWindows()
                    pioneer_mini.land()
                    break
    
                elif key == ord("5"):
                    nearby_pixels -= 10
                elif key == ord("6"):
                    nearby_pixels += 10
                elif key == ord("7"):
                    edge -= 2
                elif key == ord("8"):
                    edge += 2
    
                elif key == ord("1"):
                    pioneer_mini.arm()
                elif key == ord("2"):
                    pioneer_mini.disarm()
                elif key == ord("3"):
                    time.sleep(2)
                    pioneer_mini.arm()
                    time.sleep(1)
                    pioneer_mini.takeoff()
                    time.sleep(2)
                elif key == ord("4"):
                    time.sleep(2)
                    pioneer_mini.land()
                    time.sleep(2)
                elif key == ord("w"):
                    ch_3 = min_v
                elif key == ord("s"):
                    ch_3 = max_v
                elif key == ord("a"):
                    ch_4 = min_v
                elif key == ord("d"):
                    ch_4 = max_v
                elif key == ord("q"):
                    ch_2 = 2000
                elif key == ord("e"):
                    ch_2 = 1000
                elif key == ord("i"):
                    ch_1 = 2000
                elif key == ord("k"):
                    ch_1 = 1000
                elif key == ord("p"):
                    is_control_by_PID = not is_control_by_PID
    
                # print("ch3, ch2", ch_3, ch_2)
    
                pioneer_mini.send_rc_channels(
                    channel_1=ch_1,
                    channel_2=ch_2,
                    channel_3=ch_3,
                    channel_4=ch_4,
                    channel_5=ch_5,
                )
    
                cv2.imshow('live from your pc :)', frame_after_thresh)
                cv2.imshow('without changes', frame)
    except Exception:

        print(traceback.format_exc())
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini
